import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def fetch_poster(movie_id):
    # tmdb_api = os.getenv('TMDB_API')
    tmdb_access_token=os.getenv('TMDB_ACCESS_TOKEN')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_access_token}"
    }
    res = requests.get(url=url, headers=headers)
    data = json.loads(res.text)
    prepend_poster_path = "https://image.tmdb.org/t/p/w500"
    if data['poster_path']:
        full_poster_path = prepend_poster_path + data['poster_path']
        print(full_poster_path)
        return full_poster_path

def recommend(movie, movies_df, similarity_matrix, top_n=5):
    idx = movies_df[movies_df['title'] == movie].index[0]
    distances = list(enumerate(similarity_matrix[idx]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommend_movies = []
    recommend_movies_posters = []

    for i in sorted_movies:
        recommend_movies.append(movies_df.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movies_df.iloc[i[0]].id))

    # return [movies_df.iloc[i[0]].title for i in sorted_movies]
    return recommend_movies, recommend_movies_posters
