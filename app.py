import streamlit as st
from recommender.data_loader import load_and_clean_dataset
from recommender.vectorizer import vectorize_df
from recommender.recommender import recommend

@st.cache_data
def get_data():
    return load_and_clean_dataset()

@st.cache_resource
def get_vectorizer(movies_df):
    return vectorize_df(movies_df)

def main():
    st.title('🎬 Movie Recommender System')

    movies_df = get_data()
    similarity_matrix = get_vectorizer(movies_df)

    selected_movie_name = st.selectbox('Select a movie to get some recommendations', movies_df['title'])

    if st.button('Recommend'):
        recommended_titles, posters = recommend(selected_movie_name, movies_df, similarity_matrix)
        columns = st.columns(spec=len(recommended_titles), gap='small', vertical_alignment='center', border=False)
        for col, title, img in zip(columns, recommended_titles, posters):
            with col:
                st.write(title)
                st.image(img)

if __name__ == '__main__':
    main()
