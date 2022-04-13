from typing import Dict

from apps.cinema.constants import MAIN_CINEMARK_CINEMAS, MAIN_CINEPOLIS_CINEMAS
from apps.cinema.services import (biografo, centro_arte_alameda, cinehoyts,
                                  cinemark, normandie)


def scrapp_every_cinema() -> Dict[str, str]:
    movies = {}
    movies = biografo.scrapper(movies=movies)
    movies = centro_arte_alameda.scrapper(movies=movies)
    movies = {m: movies[m] for m in sorted(movies, key=movies.get, reverse=True)}
    for cinema_url in MAIN_CINEPOLIS_CINEMAS:
        movies = cinehoyts.scrapper(cinema_url, movies)
    for cinema_url in MAIN_CINEMARK_CINEMAS:
        movies = cinemark.scrapper(cinema_url, movies)
    movies = normandie.scrapper(movies=movies)
    movies = {m: movies[m] for m in sorted(movies, key=movies.get, reverse=True)}
    print(movies)
    return movies
