import csv
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = "Load movies from a CSV file into the database"

    def handle(self, *args, **kwargs):
        csv_file = "movies/data/movies.csv"  # Update the path if needed

        with open(csv_file, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Movie.objects.create(
                    title=row["title"],
                    overview=row["overview"],
                    genres=row["genres"]
                )

        self.stdout.write(self.style.SUCCESS("✅ Successfully loaded movies!"))
