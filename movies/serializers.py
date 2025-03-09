from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class RecommendationSerializer(serializers.Serializer):
    title = serializers.CharField()
    overview = serializers.CharField()
