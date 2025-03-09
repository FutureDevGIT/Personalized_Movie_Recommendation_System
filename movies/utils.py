import requests
from .models import Movie
from django.conf import settings

TMDB_API_KEY = "20638e64d55d4bead3f42793f5551c6e"

def fetch_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])

        for movie in movies:
            genres = [str(genre) for genre in movie.get("genre_ids", [])]  # Store genre IDs
            genre_string = ",".join(genres)

            Movie.objects.update_or_create(
                title=movie["title"],
                defaults={
                    "overview": movie["overview"],
                    "release_date": movie.get("release_date"),
                    "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                    "rating": movie["vote_average"],
                    "genres": genre_string,
                },
            )
        return "Movies updated successfully!"
    return "Failed to fetch movies."

