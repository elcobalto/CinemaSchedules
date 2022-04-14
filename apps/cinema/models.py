from django.db import models

from apps.movie.models import Movie


class Cinema(models.Model):
    CINEHOYTS = "CineHoyts"
    CINEMARK = "Cinemark"
    CINEPLANET = "Cineplanet"
    INDEPENDENT = "Independent"
    MUVIX = "Muvix"
    CHAIN_CHOICES = (
        (CINEHOYTS, CINEHOYTS),
        (CINEMARK, CINEMARK),
        (CINEPLANET, CINEPLANET),
        (INDEPENDENT, INDEPENDENT),
        (MUVIX, MUVIX),
    )
    chain = models.CharField(max_length=255, choices=CHAIN_CHOICES)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)


class Schedule(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    showing_datetime = models.CharField(max_length=255)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    week = models.DateTimeField()
