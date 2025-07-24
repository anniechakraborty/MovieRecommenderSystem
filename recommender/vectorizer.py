from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def vectorize_df(df):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix
