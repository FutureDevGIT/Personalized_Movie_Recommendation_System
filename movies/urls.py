from  django.urls import path
from .views import MovieListView, RecommendMoviesView

urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movies-list"),
    path("recommend/", RecommendMoviesView.as_view(), name="recommend-movies"),
]
