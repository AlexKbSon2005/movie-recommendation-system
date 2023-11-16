import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    return data.json()

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:11]:  # Changed from [1:6] to [1:11]
        movie_id = movies.iloc[i[0]].movie_id
        movie_details = fetch_movie_details(movie_id)
        movie_info = {
            'title': movie_details['title'],
            'overview': movie_details['overview'],
            'release_date': movie_details['release_date'],
            'poster_path': fetch_poster(movie_id)
        }
        recommended_movies.append(movie_info)

    return recommended_movies

st.header('Movie Recommender System')
st.markdown('by Laxman Acharya')
movies = pickle.load(open(r'D:\movie_recommender\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'D:\movie_recommender\similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select or type your movie here",
    movie_list
)

if st.button('See Similar Movies'):
    recommended_movies = recommend(selected_movie)

    # Divide recommended movies into two lists for two columns
    col1, col2 = st.columns(2)

    for i, movie in enumerate(recommended_movies):
        # Alternate between the two columns
        if i % 2 == 0:
            with col1:
                st.subheader(movie['title'])
                st.text(f"Release Date: {movie['release_date']}")
                st.image(movie['poster_path'])
                st.text(movie['overview'])
                st.write("---")
        else:
            with col2:
                st.subheader(movie['title'])
                st.text(f"Release Date: {movie['release_date']}")
                st.image(movie['poster_path'])
                st.text(movie['overview'])
                st.write("---")
