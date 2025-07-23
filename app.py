import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utility import extract_genres_keywords, extract_cast, get_director_name, stem_text

def load_and_clean_dataset():
    # ------------------------------
    # DATA LOADING
    # ------------------------------
    movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
    print(movies.head(1))
    print()
    credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
    print(credits.head(1))
    print()
    # Merging the datasets based on the title column
    movies = movies.merge(credits, on='title')
    print(f'Merged movies and credit DFs. Shape of the merged DF: {movies.shape}')
    print('Merged DF Info:')
    print(movies.info())
    print('Language distribution of movies')
    print(movies['original_language'].value_counts())
    print()
    print('Unique languages present')
    print(movies['original_language'].nunique())
    print()

    # ------------------------------
    # DATA CLEANING
    # ------------------------------
    movies_cleaned = movies[['id', 'genres', 'keywords', 'title', 'overview', 'cast', 'crew']]
    print('Counting number of NULL VALUES')
    print(movies_cleaned.isnull().sum())
    movies_cleaned.dropna(inplace=True)
    movies_cleaned.duplicated().sum()

    # Cleaning the genres and keywords column
    movies_cleaned['genres'] = movies_cleaned['genres'].apply(extract_genres_keywords)
    movies_cleaned['keywords'] = movies_cleaned['keywords'].apply(extract_genres_keywords)
    # Extracting the names of the top 5 actors from the cast column
    movies_cleaned['cast'] = movies_cleaned['cast'].apply(extract_cast)
    # Extracting the director name from the crew set
    movies_cleaned['crew'] = movies_cleaned['crew'].apply(get_director_name)
    print('Cleaned dataset')
    print(movies_cleaned.head())
    print()

    # ------------------------------
    # DATA PREPROCESSING
    # ------------------------------
    # Replacing the space between names and keywords to combine them into a single entity
    movies_cleaned['genres'] = movies_cleaned['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
    movies_cleaned['keywords'] = movies_cleaned['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
    movies_cleaned['cast'] = movies_cleaned['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
    # Removing null values from crew
    movies_cleaned['crew'] = movies_cleaned['crew'].fillna('[Unknown]')
    movies_cleaned['crew'] = movies_cleaned['crew'].apply(lambda x:[i.replace(" ", "") for i in x])
    movies_cleaned['overview'] = movies_cleaned['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])
    # Creating the tags column (list) by combining the overview, genres, keywords, cast and crew columns
    movies_cleaned['tags'] = movies_cleaned['overview'] + movies_cleaned['genres'] + movies_cleaned['keywords'] + movies_cleaned['cast'] + movies_cleaned['crew']

    # Creating a new movies dataframe using the cleaned columns for further processing
    movies_df = movies_cleaned[['id', 'title', 'tags']]

    # Creating a string from the list by joining every elemnet in tag with a space
    movies_df['tags'] = movies_df['tags'].apply(lambda x:" ".join(x))
    movies_df['tags'] = movies_df['tags'].apply(lambda x:x.lower())

    # We apply STEMMING to ensure that words like 'actions', 'action' etc. get grouped into one category as they have the same base word.
    # Similarly, words like 'loved', 'loving', 'loves' get grouped under 'love'.
    movies_df['tags'] = movies_df['tags'].apply(stem_text)

    return movies_df


def vectorize_df(df):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity_matrix = cosine_similarity(vectors)
    print('Shape of the similarity matrix generated: ', similarity_matrix.shape)
    return similarity_matrix

# # Returns 5 similar movies for the provided movie
# def recommend(movie, similarity_matrix):
#     # Fetching the index of the movie
#     movie_index = movies_df[movies_df['title'] == movie].index[0]
    
#     # Getting the vector distances for this movie from the similarity matrix
#     distances = similarity_matrix[movie_index]

#     # Sorting the distances to find the top 5 similar movies
#     sorted_distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])

#     top_5_movies = sorted_distances[1:6]
#     for i in top_5_movies:
#         print(movies_df.iloc[i[0]].title)
#         print(i[0])
#     # return top_5_movies



def create_app(movies_df, similarity_matrix):
    st.title('🎬 Movie Recommender System')
    selected_movie_name = st.selectbox('Select a movie to get some recommendations', movies_df['title'])

    if st.button('Recommend'):
        # Fetching the index of the movie
        movie_index = movies_df[movies_df['title'] == selected_movie_name].index[0]
        
        # Getting the vector distances for this movie from the similarity matrix
        distances = similarity_matrix[movie_index]

        # Sorting the distances to find the top 5 similar movies
        sorted_distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])

        top_5_movies = sorted_distances[1:6]
        for i in top_5_movies:
            st.write(movies_df.iloc[i[0]].title)

if __name__ == '__main__':
    movies_df = load_and_clean_dataset()
    similarity_matrix = vectorize_df(df=movies_df)

    create_app(movies_df=movies_df, similarity_matrix=similarity_matrix)
