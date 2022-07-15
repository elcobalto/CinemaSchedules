from django.db.models import Q

from apps.cinema.models import Cinema, Town, Showing
from apps.movie.models import Movie
from apps.cinema.services.cinehoyts.services import update as cinehoyts_update
from apps.cinema.services.cinemark.services import update as cinemark_update


def get_showings(
        movie_title: str = None,
        showdate: str = None,
        cinema_filter: str = None,
        format: str = None,
):
    showings = Showing.objects.filter().all()
    if movie_title:
        showings = showings.filter(movie__title=movie_title).all()
    if showdate:
        showings = showings.filter(showing_date=showdate).all()
    if format:
        showings = showings.filter(format__contains=format).all()
    if cinema_filter:
        showings = showings.filter(
            Q(cinema__name__contains=cinema_filter) |
            Q(cinema__chain__contains=cinema_filter) |
            Q(cinema__town__name__contains=cinema_filter) |
            Q(cinema__town__city__contains=cinema_filter) |
            Q(cinema__town__region__contains=cinema_filter) |
            Q(cinema__town__zone__contains=cinema_filter)
        ).all()
    return showings


def get_cinemas(
        movie_title: str = None,
        showdate: str = None,
        cinema_filter: str = None,
        format: str = None,
):
    cinemas = Cinema.objects.filter().all()
    if movie_title:
        cinemas = cinemas.filter(showings__movie__title=movie_title).all()
    if showdate:
        cinemas = cinemas.filter(showings__showing_date=showdate).all()
    if format:
        cinemas = cinemas.filter(showings__format__contains=format).all()
    if cinema_filter:
        cinemas = cinemas.filter(
            Q(name__contains=cinema_filter) |
            Q(chain__contains=cinema_filter) |
            Q(town__name__contains=cinema_filter) |
            Q(town__city__contains=cinema_filter) |
            Q(town__region__contains=cinema_filter) |
            Q(town__zone__contains=cinema_filter)
        ).all()
    return cinemas


def get_movies(
        movie_title: str = None,
        showdate: str = None,
        cinema_filter: str = None,
        format: str = None,
):
    movies = Movie.objects.filter().all()
    if movie_title:
        movies = movies.filter(title=movie_title).all()
    if showdate:
        movies = movies.filter(showings__showing_date=showdate).all()
    if format:
        movies = movies.filter(showings__format__contains=format).all()
    if cinema_filter:
        movies = movies.filter(
            Q(showings__cinema__name__contains=cinema_filter) |
            Q(showings__cinema__chain__contains=cinema_filter) |
            Q(showings__cinema__town__name__contains=cinema_filter) |
            Q(showings__cinema__town__city__contains=cinema_filter) |
            Q(showings__cinema__town__region__contains=cinema_filter) |
            Q(showings__cinema__town__zone__contains=cinema_filter)
        ).all()
    return movies


def update():
    print("Starting to update!")
    cinehoyts_update()
    cinemark_update()
    print("Finishing updating!")
