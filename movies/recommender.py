import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie as MovieModel
from tmdbv3api import TMDb, Movie
from difflib import get_close_matches

tmdb = TMDb()
tmdb.api_key = "20638e64d55d4bead3f42793f5551c6e"

movie_api = Movie()

def get_movie_details(movie_title):
    """Fetch movie details (poster, release date, rating, genres) from TMDb API."""
    search_results = movie_api.search(movie_title)
    if search_results:
        movie_data = search_results[0]
        # Fetch full movie details using movie ID
        movie_details = movie_api.details(movie_data.id)
        poster_url = f"https://image.tmdb.org/t/p/w500{movie_data.poster_path}" if movie_data.poster_path else None
        genres = [genre["name"] for genre in movie_details.genres] if hasattr(movie_details, "genres") else []
        return {
            "poster": poster_url,
            "release_date": movie_data.release_date if hasattr(movie_data, "release_date") else "N/A",
            "rating": movie_data.vote_average if hasattr(movie_data, "vote_average") else "N/A",
            "genres": genres
        }
    return {"poster": None, "release_date": "N/A", "rating": "N/A", "genres": []}

def find_closest_match(movie_title, movie_list):
    """Find the closest match from a list of movie titles."""
    matches = get_close_matches(movie_title, movie_list, n=1, cutoff=0.6)  # ✅ Finds best match with a threshold
    return matches[0] if matches else None

def get_recommendations(movie_title, num_recommendations=8):
    """Generate recommendations using a large movie dataset."""
    movies = list(MovieModel.objects.all().values("id", "title", "overview", "genres"))
    df = pd.DataFrame(movies)

    if df.empty:
        return []

    df["features"] = df["overview"].fillna("") + " " + df["genres"].fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["features"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

     # Normalize titles to lowercase
    df["title"] = df["title"].str.lower()
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

    # Fuzzy matching to handle small spelling differences
    closest_match = find_closest_match(movie_title.lower(), df["title"].tolist())
    if closest_match:
        idx = indices.get(closest_match)
        print(f"✅ Found closest match: {closest_match}")
    else:
        print("⚠️ No close match found!")
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