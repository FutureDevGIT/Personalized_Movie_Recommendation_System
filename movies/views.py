from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .recommender import get_recommendations


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class RecommendMoviesView(APIView):
    def get(self, request):
        movie_title = request.query_params.get("title")
        if not movie_title:
            return Response({"error": "Movie title is required"}, status=400)

        recommendations = get_recommendations(movie_title)
        return Response({"recommendations": recommendations})