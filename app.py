import streamlit as st
import pickle
import pandas as pd
st.title("Movie Recommendation System")
st.write("This is a simple movie recommendation system.")
movies=pickle.load(open('movies_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies_df=pd.DataFrame(movies)
movie_list=movies_df['title'].values
selected_movie=st.selectbox("Type or select a movie from the dropdown",movie_list)
def recommend(movie):
    movie_index=movies_df[movies_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
    return recommended_movies

if st.button('Show Recommendation'):
    recommendations=recommend(selected_movie)
    for i in recommendations:
        st.write(i)
# You can replace 'Avatar' with any movie title present in your dataset to get recommendations.
