from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, Tuple

from apps.cinema.models import Showing
from apps.movie.models import Movie


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def clean_movie_title(movie: str) -> str:
    return movie.replace("PELICULA", "").replace("MOVIE", "")


def similar_movies(movie: str, possible_movie: str) -> bool:
    clean_movie = clean_movie_title(movie)
    clan_possible = clean_movie_title(possible_movie)
    similarity = similar(clean_movie, clan_possible)
    is_substring = (
        clean_movie in clan_possible
        if len(clean_movie) < len(clan_possible)
        else clan_possible in clean_movie
    )
    if not is_substring:
        similarity = similar(clean_movie, clan_possible)
    return is_substring or similarity > 0.5


def movie_exists(movie: str, movies: Dict[str, str]) -> Tuple[bool, str]:
    for possible in movies.keys():
        if similar_movies(movie, possible):
            return True, possible
    return False, movie


def check_if_movie_exists(movie: str):
    return (
        Movie.objects.filter(title__icontains=movie).exists()
        or Movie.objects.filter(alternative_title__icontains=movie).exists()
    )


def save_movie_and_schedule(movie, current_cinema, schedule, week=None):
    does_movie_exist = check_if_movie_exists(movie)
    today = datetime.today().strftime("%Y-%m-%d")
    if not week:
        week = today
    if does_movie_exist:
        movie_object = Movie.objects.filter(title__icontains=movie).first()
        if not movie_object:
            movie_object = Movie.objects.filter(
                alternative_title__icontains=movie
            ).first()
    else:
        movie_object = Movie(title=movie, release_date=today)
        movie_object.save()
    new_schedule = Showing(
        movie=movie_object,
        cinema=current_cinema,
        showing_datetime=schedule,
        week=week,
    )
    new_schedule.save()
