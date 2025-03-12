import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie
from tmdbv3api import TMDb, Movie as TMDbMovie

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = "20638e64d55d4bead3f42793f5551c6e"

movie_api = TMDbMovie()


def get_movie_poster(movie_title):
    """Fetch the movie poster URL using TMDb API."""
    try:
        search_results = movie_api.search(movie_title)
        if search_results:
            poster_path = search_results[0].poster_path
            return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
    return None


def get_recommendations(movie_title, num_recommendations=8):
    """Get movie recommendations based on text similarity (TF-IDF)."""

    # Fetch movie data from the database
    movies = list(Movie.objects.all().values("id", "title", "overview", "genres"))
    df = pd.DataFrame(movies)

    if df.empty:
        return []

    # Combine 'overview' and 'genres' for better recommendations
    df["features"] = df["overview"].fillna("") + " " + df["genres"].fillna("")

    # Convert text to vectors using TF-IDF
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["features"])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the given movie
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
    idx = indices.get(movie_title)

    if idx is None:
        return []

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]  # Exclude the first (self) match

    # Get recommended movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Fetch movie details and posters
    recommended_movies = []
    for _, row in df.iloc[movie_indices].iterrows():
        recommended_movies.append({
            "title": row["title"],
            "overview": row["overview"],
            "poster": get_movie_poster(row["title"]) or "https://via.placeholder.com/300"
        })

    return recommended_movies
