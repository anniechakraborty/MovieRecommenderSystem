import pandas as pd
from utils.utility import extract_genres_keywords, extract_cast, get_director_name, stem_text

def load_and_clean_dataset():
    movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
    credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
    movies = movies.merge(credits, on='title')

    movies_cleaned = movies[['id', 'genres', 'keywords', 'title', 'overview', 'cast', 'crew']].dropna()

    movies_cleaned['genres'] = movies_cleaned['genres'].apply(extract_genres_keywords)
    movies_cleaned['keywords'] = movies_cleaned['keywords'].apply(extract_genres_keywords)
    movies_cleaned['cast'] = movies_cleaned['cast'].apply(extract_cast)
    movies_cleaned['crew'] = movies_cleaned['crew'].apply(get_director_name)
    movies_cleaned['crew'] = movies_cleaned['crew'].fillna('[Unknown]')

    movies_cleaned['genres'] = movies_cleaned['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_cleaned['keywords'] = movies_cleaned['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_cleaned['cast'] = movies_cleaned['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_cleaned['crew'] = movies_cleaned['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies_cleaned['overview'] = movies_cleaned['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

    movies_cleaned['tags'] = movies_cleaned['overview'] + movies_cleaned['genres'] + movies_cleaned['keywords'] + movies_cleaned['cast'] + movies_cleaned['crew']
    movies_df = movies_cleaned[['id', 'title', 'tags']]
    movies_df['tags'] = movies_df['tags'].apply(lambda x: " ".join(x).lower())
    movies_df['tags'] = movies_df['tags'].apply(stem_text)

    return movies_df
