from django.db import models

from apps.movie.models import Movie


class Town(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)


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
    town = models.ForeignKey(
        Town,
        on_delete=models.CASCADE,
        related_name="cinemas",
        blank=True,
        null=True,
    )


class Showing(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name="showings",
    )
    format = models.CharField(max_length=255, blank=True, null=True)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="showings",
    )
    showing_date = models.CharField(max_length=255)
    showing_datetime = models.CharField(max_length=255)
