# 🎬 Movie Recommender System

A simple yet powerful movie recommender system built using **Pandas**, **scikit-learn**, and **Streamlit**. It recommends similar movies based on genre, cast, keywords, and plot descriptions using natural language processing and cosine similarity.

---

## 📌 Features

- Recommends top 5 similar movies based on a selected title.
- Processes and cleans movie metadata (genres, cast, keywords, etc.).
- Vectorizes movie tags using CountVectorizer.
- Optimized with caching to avoid redundant computation on user interactions.
- Built with a clean, interactive UI using Streamlit.

---

## 🧠 How It Works

1. **Data Loading**: Merges movie and credit datasets from TMDB.
2. **Preprocessing**: Extracts important features like genres, cast, and director.
3. **Tag Creation**: Combines relevant features into a single text field.
4. **Vectorization**: Uses `CountVectorizer` to transform text into numeric vectors.
5. **Similarity Matrix**: Computes cosine similarity between movie vectors.
6. **Recommendation**: Retrieves top 5 most similar movies.

---

## 🚀 Demo

Run locally:

```bash
git clone https://github.com/yourusername/movie-recommender.git
cd movie-recommender
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```bash
movie_recommender/
│
├── app.py                      # Streamlit app entry point
├── requirements.txt
├── data/                       # Raw TMDB datasets (CSV)
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── recommender/
│   ├── data_loader.py          # Loads & preprocesses data
│   ├── vectorizer.py           # Vectorizes movie tags
│   ├── recommender.py          # Movie recommendation logic
│
├── utils/
│   └── text_utils.py           # NLP helpers: stemming, extraction
│
└── tests/
    └── test_recommender.py     # Unit tests

```

## 📚 Data Source
This project uses the TMDB 5000 Movie Dataset from Kaggle.

## 🛡 License
This project is open-source under the MIT License.

## 👨‍💻 Author
Inspired by [CampusX's Movie Recommendation System](https://youtu.be/1xtrIEwY_zY?si=hm_TQAS-E2_O07UT) and built by [Annie Chakraborty](https://github.com/anniechakraborty). Contributions welcome!