import streamlit as st
import pickle
import pandas as pd
import requests
import os

# --- Load Data ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_dict = pickle.load(open(os.path.join(BASE_DIR, 'movie_dict.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))

# --- TMDB API KEY ---
API_KEY = "YOUR_API_KEY_HERE"

# --- Fetch Poster ---
import requests
import time

def fetch_poster(movie_id):
    API_KEY = "9341ea199e1e7a17616ba4870bfd20d8"

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        time.sleep(0.3)  # 🔥 VERY IMPORTANT (prevents blocking)

        if response.status_code != 200:
            return "https://via.placeholder.com/300x450?text=No+Poster"

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=API+Blocked"
# --- Recommendation Function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:15]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        poster = fetch_poster(movie_id)

        # ✅ Only add if poster is valid
        if "placeholder" not in poster:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(poster)

        # stop after 5 valid movies
        if len(recommended_movies) == 5:
            break

    return recommended_movies, recommended_posters

# --- UI ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])