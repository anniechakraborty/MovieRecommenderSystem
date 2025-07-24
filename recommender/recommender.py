def recommend(movie, movies_df, similarity_matrix, top_n=5):
    idx = movies_df[movies_df['title'] == movie].index[0]
    distances = list(enumerate(similarity_matrix[idx]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:top_n+1]
    return [movies_df.iloc[i[0]].title for i in sorted_movies]
