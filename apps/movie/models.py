from django.db import models


class Movie(models.Model):
    alternative_title = models.CharField(max_length=255, blank=True, null=True)
    imdb_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, unique=True)
    release_date = models.DateTimeField(blank=True, null=True)
