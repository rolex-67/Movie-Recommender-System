import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    # Note: Replace <<api_key>> with your actual TMDB API Key
    url = "https://api.themoviedb.org/3/movie/{}?api_key=http://www.omdbapi.com/?i=tt3896198&apikey=958a9109&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    # Adding a fallback in case poster_path is missing
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Poster+Found"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         key=lambda x: x[1],
                         reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']   # FIX HERE
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters
# 1. Load the data
# Load Data
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')



option = st.selectbox(
    "Search Movie List",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(option)
    
    # Create 5 columns for the 5 recommendations
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])