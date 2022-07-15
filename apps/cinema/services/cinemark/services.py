from typing import Any, Dict, List

import requests
from django.db.models import Q

from apps.cinema.models import Cinema, Showing
from apps.movie.models import Movie

CINEMARK_HOST = "https://api.cinemark.cl/api/"


def get_showings_response_by_cinema_id(
    cinema_id: int = 512,
) -> List[Dict[str, Any]]:
    try:
        showings = requests.get(
            f"{CINEMARK_HOST}/vista/data/billboard?cinema_id={cinema_id}"
        )
        clean_showings = showings.json()
        return clean_showings
    except Exception:
        return []


def _get_formatted_format(format: str):
    format = format.replace('DOB', 'ESP')
    format = format.replace('SUBT', 'SUB')
    return format


def update():
    cinemas = Cinema.objects.filter(chain=Cinema.CINEMARK).all()
    for cinema in cinemas:
        cinema_showings = get_showings_response_by_cinema_id(cinema.keyword)
        for showing_date in cinema_showings:
            showdate = showing_date["date"]
            movies_showing = showing_date["movies"]
            for movie_showing in movies_showing:
                movie_title = movie_showing["title"].upper()
                movie_formats = movie_showing["movie_versions"]
                movie = Movie.objects.filter(
                    Q(title__in=movie_title)
                    | Q(title__contains=movie_title)
                    | Q(alternative_title__in=movie_title)
                    | Q(alternative_title__contains=movie_title)
                ).first()
                if not movie:
                    movie = Movie(title=movie_title, release_date=showdate)
                    movie.save()
                for movie_format in movie_formats:
                    movie_showtimes = movie_format["sessions"]
                    showtime_format = _get_formatted_format(movie_format["title"][len(movie_title) + 2: -1])
                    for movie_showtime in movie_showtimes:
                        showtime = movie_showtime["hour"][:-3]
                        if not Showing.objects.filter(
                            cinema=cinema,
                            format=showtime_format,
                            movie=movie,
                            showing_date=showdate,
                            showing_datetime=showtime,
                        ).exists():
                            new_showing = Showing(
                                cinema=cinema,
                                format=showtime_format,
                                movie=movie,
                                showing_date=showdate,
                                showing_datetime=showtime,
                            )
                            new_showing.save()
