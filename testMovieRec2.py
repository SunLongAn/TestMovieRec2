# AUTOGENERATED! DO NOT EDIT! File to edit: testMovieRec2.ipynb.

# %% auto 0
__all__ = []

# %% testMovieRec2.ipynb 0
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# %% testMovieRec2.ipynb 3
st.title(":blue[Fanz O' Filmz] Movie Recommender")

# %% testMovieRec2.ipynb 4
df = pd.read_csv('data/IMDb_All_Genres_etf_clean1.csv')

# %% testMovieRec2.ipynb 5
movies = df[['Movie_Title', 'Year', 'Director', 'Actors', 'main_genre', 'side_genre']].copy()

# %% testMovieRec2.ipynb 6
# combine genre columns
def combine_genres(data):
    comb_genres = []
    for i in range(0, data.shape[0]):
        comb_genres.append(data['main_genre'][i] + ' ' + data['side_genre'][i])
        
    return comb_genres

# %% testMovieRec2.ipynb 7
movies['side_genre'] = movies['side_genre'].str.replace(",","")

# %% testMovieRec2.ipynb 8
movies['genres'] = combine_genres(movies)

# %% testMovieRec2.ipynb 9
movies = movies.drop(columns = ['main_genre', 'side_genre'])

# %% testMovieRec2.ipynb 10
# combine Movie_Title and Year columns to make unique titles in the case of different movies having the same name
def get_clean_title(data):
    clean_title = []
    for i in range(0, data.shape[0]):
        clean_title.append(data['Movie_Title'][i] + ' (' + str(data['Year'][i]) + ')')
        
    return clean_title

# %% testMovieRec2.ipynb 11
movies['clean_title'] = get_clean_title(movies)

# %% testMovieRec2.ipynb 12
movies = movies.drop_duplicates(subset=['clean_title']).copy()

# %% testMovieRec2.ipynb 14
movies.reset_index(inplace = True, drop = True)

# %% testMovieRec2.ipynb 16
movies['Director'] = movies["Director"].str.replace("Directors:", "")
movies['Director'] = movies['Director'].map(lambda x: x.replace(" ", "").lower().split(',')[:3])

movies['Actors'] = movies['Actors'].map(lambda x: x.replace(" ", "").lower().split(',')[:4])

movies['genres'] = movies['genres'].map(lambda x: x.lower().split())

# %% testMovieRec2.ipynb 22
y = 2000

# %% testMovieRec2.ipynb 23
def round_down(year):
    return year - (year%10)

round_down(y)

# %% testMovieRec2.ipynb 24
movies['decade'] = movies['Year'].apply(round_down)

# %% testMovieRec2.ipynb 26
movies['Director'] = movies['Director'].str.join(" ")

movies['Actors'] = movies['Actors'].str.join(" ")

movies['genres'] = movies['genres'].str.join(" ")

# %% testMovieRec2.ipynb 27
# combine features
def combine_features(data):
    combined_features = []
    for i in range(0, data.shape[0]):
        combined_features.append(str(data['decade'][i]) + ' ' +
                                  data['genres'][i] + ' ' +
                                  data['Actors'][i] + ' ' +
                                  data['Director'][i])
        
    return combined_features

# %% testMovieRec2.ipynb 28
movies['combined_features'] = combine_features(movies)

# %% testMovieRec2.ipynb 30
tfvec = TfidfVectorizer()
tfvec_matrix = tfvec.fit_transform(movies['combined_features'])

# %% testMovieRec2.ipynb 31
cs = cosine_similarity(tfvec_matrix)

# %% testMovieRec2.ipynb 33
def recommend(movie):
    movie_indices = movies[movies['clean_title'] == movie].index[0]
    distances = cs[movie_indices]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].clean_title)

    return recommended_movies

# %% testMovieRec2.ipynb 35
selected_movie_name = st.selectbox('Please select a movie you enjoy:', movies['clean_title'].values)

# %% testMovieRec2.ipynb 36
if st.button('Get Recommendations'):
    recommendations = recommend(selected_movie_name)
    st.write("Based on your selection, we recommend the following movies:")
    for j in recommendations:
        st.write(j)
