import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie as MovieModel
from tmdbv3api import TMDb, Movie

tmdb = TMDb()
tmdb.api_key = "20638e64d55d4bead3f42793f5551c6e"

movie_api = Movie()

def get_movie_details(movie_title):
    """Fetch movie details (poster, release date, rating, genres) from TMDb API."""
    search_results = movie_api.search(movie_title)
    if search_results:
        movie_data = search_results[0]
        poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.poster_path}" if movie_data.poster_path else None
        genres = [genre["name"] for genre in movie_data.genres] if hasattr(movie_data, "genres") else []
        return {
            "poster": poster_url,
            "release_date": movie_data.release_date if hasattr(movie_data, "release_date") else "N/A",
            "rating": movie_data.vote_average if hasattr(movie_data, "vote_average") else "N/A",
            "genres": genres
        }
    return {"poster": None, "release_date": "N/A", "rating": "N/A", "genres": []}

def get_recommendations(movie_title, num_recommendations=8):
    """Get movie recommendations with additional details."""
    movies = list(MovieModel.objects.all().values("id", "title", "overview", "genres"))  # Use MovieModel here
    df = pd.DataFrame(movies)

    if df.empty:
        return []

    df["features"] = df["overview"].fillna("") + " " + df["genres"].fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
    idx = indices.get(movie_title)

    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
    movie_indices = [i[0] for i in sim_scores]

    recommended_movies = []
    for index in movie_indices:
        movie_info = df.iloc[index][["title", "overview"]].to_dict()
        details = get_movie_details(movie_info["title"])
        movie_info.update(details)
        recommended_movies.append(movie_info)

    return recommended_movies
