import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
movies_df=pd.read_csv('movies.csv')
credit_df=pd.read_csv('credits.csv')
movies_df=movies_df.merge(credit_df,on='title')
movies_df=movies_df[['movie_id','title','overview','genres','keywords','cast','crew']]

movies_df.dropna(inplace=True)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies_df['genres']=movies_df['genres'].apply(convert)
movies_df['keywords']=movies_df['keywords'].apply(convert)


def convert(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L
movies_df['cast']=movies_df['cast'].apply(convert)
def crewConvert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L
movies_df['crew']=movies_df['crew'].apply(crewConvert)
movies_df['genres']=movies_df['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['keywords']=movies_df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['cast']=movies_df['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['crew']=movies_df['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['overview']=movies_df['overview'].apply(lambda x:x.split())
movies_df['tags']=movies_df['overview']+movies_df['genres']+movies_df['keywords']+movies_df['cast']+movies_df['crew']
movies_df=movies_df[['movie_id','title','tags']]
movies_df['tags']=movies_df['tags'].apply(lambda x:" ".join(x))
movies_df['tags']=movies_df['tags'].apply(lambda x:x.lower())
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(movies_df['tags']).toarray()
print(cv.get_feature_names_out())
similarity=cosine_similarity(vectors)
print(similarity)
# You can replace 'Avatar' with any movie title present in your dataset to get recommendations.
# Save the model and data for future use
import pickle
pickle.dump(movies_df.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
