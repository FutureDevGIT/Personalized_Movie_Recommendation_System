from django.core.management.base import BaseCommand
from movies.utils import fetch_movies

class Command(BaseCommand):
    help = "Fetch movies from TMDb API and store in the database"

    def handle(self, *args, **kwargs):
        result = fetch_movies()
        self.stdout.write(self.style.SUCCESS(result))
