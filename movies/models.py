from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.URLField(max_length=500, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    genres = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
