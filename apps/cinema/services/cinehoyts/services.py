from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from django.db.models import Q

from apps.cinema.models import Cinema, Showing
from apps.movie.models import Movie

CINEHOYTS_HOST = "https://cinehoyts.cl"

TOWN_KEYWORDS = [
    "norte-y-centro-de-chile",
    "santiago-centro",
    "santiago-oriente",
    "santiago-norte-y-poniente",
    "santiago-sur",
    "sur-de-chile",
]

month_to_number = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def get_showings_response_by_town_keyword(
    town_keyword: str = "santiago-oriente",
) -> List[Dict[str, Any]]:
    try:
        payload = {"claveCiudad": town_keyword, "esVIP": True}
        showings = requests.post(
            f"{CINEHOYTS_HOST}/Cartelera.aspx/GetNowPlayingByCity", json=payload
        )
        clean_showings = showings.json()
        return clean_showings["d"]["Cinemas"]
    except Exception:
        return []


def _get_showdate(showtime_date: str):
    day, month = showtime_date.split(" ")
    return datetime(year=2022, month=month_to_number[month], day=int(day)).date()


def _get_formatted_format(format: str):
    if format == 'ESP':
        return '2D ESP'
    if format == 'SUBT':
        return '2D SUB'
    format = format.replace('DOB', 'ESP')
    format = format.replace('SUBT', 'SUB')
    return format


def update():
    for town_keyword in TOWN_KEYWORDS:
        cinemas_showings = get_showings_response_by_town_keyword(town_keyword)
        for cinema_showings in cinemas_showings:
            cinema_keyword = cinema_showings["Key"]
            cinema = Cinema.objects.get(keyword=cinema_keyword)
            for showing_date in cinema_showings["Dates"]:
                showdate = _get_showdate(showing_date["ShowtimeDate"])
                for movie_showing in showing_date["Movies"]:
                    movie_title = movie_showing["Title"].upper()
                    movie_formats = movie_showing["Formats"]
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
                        showtime_format = _get_formatted_format(movie_format["Name"])
                        for movie_showtime in movie_format["Showtimes"]:
                            showtime = movie_showtime["Time"]
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
