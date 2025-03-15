from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Movie Recommendation System API!"})

urlpatterns = [
    path("", home, name="home"),  # Default homepage
    path('admin/', admin.site.urls),
    path("api/", include("movies.urls")),  # Movie APIs
]
