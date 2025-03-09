import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Movie

def get_recommendations(movie_title, num_recommendations=5):
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
    sim_scores = sim_scores[1:num_recommendations + 1]

    # Get recommended movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return recommended movies
    recommended_movies = df.iloc[movie_indices][["title", "overview"]].to_dict(orient="records")
    return recommended_movies
