from django.db import models
from apps.movie.models import Movie


class Cinema(models.Model):
    chain = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    title = models.CharField(max_length=255)


class Schedules(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
    )
