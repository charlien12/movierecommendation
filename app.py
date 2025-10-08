import streamlit as st

import pickle

import pandas as pd

import requests

# -----------------------------

# Function to fetch movie poster

# -----------------------------

def fetch_poster(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

        data = requests.get(url)

        data.raise_for_status()

        data = data.json()

        poster_path = data.get('poster_path')

        if poster_path:

            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"

            return full_path

        else:

            return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:

        return "https://via.placeholder.com/500x750?text=No+Image"

# -----------------------------

# Streamlit UI

# -----------------------------

st.title("🎬 Movie Recommendation System")

st.write("Select a movie and get similar recommendations!")

# Load data

movies = pickle.load(open('movies_dict.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_df = pd.DataFrame(movies)

# Dropdown list

movie_list = movies_df['title'].values

selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# -----------------------------

# Recommendation function

# -----------------------------

def recommend(movie):

    movie_index = movies_df[movies_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    recommended_movie_posters = []

    for i in movies_list:

        movie_id = movies_df.iloc[i[0]].movie_id

        recommended_movies.append(movies_df.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

# -----------------------------

# Display recommendations

# -----------------------------

if st.button('Show Recommendation'):

    recommended_movies, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.text(recommended_movies[idx])

            st.image(recommended_movie_posters[idx])
 