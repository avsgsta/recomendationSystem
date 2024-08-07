import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
ratings = pd.read_csv('assets/rating.csv')
movies = pd.read_csv('assets/movies.csv')

# Preprocessing
def preprocess_data():
    # Mengubah genre menjadi list
    movies['genres'] = movies['genres'].str.split('|')
    return movies

movies = preprocess_data()

def recommend_movies_by_genre(selected_genre, num_recommendations):
    # Filter film berdasarkan genre
    genre_filtered = movies[movies['genres'].apply(lambda x: selected_genre in x)]
    
    # Mengurutkan film berdasarkan rating rata-rata jika ada
    if not genre_filtered.empty:
        genre_filtered['average_rating'] = genre_filtered['movieId'].map(ratings.groupby('movieId')['rating'].mean())
        recommendations = genre_filtered.sort_values('average_rating', ascending=False)
        return recommendations[['title', 'average_rating']].head(num_recommendations)
    else:
        return pd.DataFrame(columns=['title', 'average_rating'])

# Streamlit app
st.title('Film Recommendation System by Genre')

# Daftar genre yang tersedia
all_genres = sorted(set(g for sublist in movies['genres'].tolist() for g in sublist))
selected_genre = st.selectbox('Select Genre:', all_genres)
num_recommendations = st.slider('Number of Recommendations:', min_value=1, max_value=100, value=5)

if st.button('Get Recommendations'):
    if selected_genre and num_recommendations:
        recommendations = recommend_movies_by_genre(selected_genre, num_recommendations)
        if recommendations.empty:
            st.write('No recommendations available for the selected genre.')
        else:
            st.write('Recommendations:')
            st.write(recommendations)
    else:
        st.write('Please select a genre and number of recommendations.')
