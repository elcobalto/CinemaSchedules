import time
from typing import Dict, List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from .constants import (
    CINEMARK_PORTAL_NUNOA_URL,
    CINEPOLIS_LA_REINA_URL,
    MAIN_CINEMARK_CINEMAS,
    MAIN_CINEPOLIS_CINEMAS,
)


def scrapp_cinehoyts_schedules(
    cinema_link: str = CINEPOLIS_LA_REINA_URL, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = page.split("originalTitle=")
    for raw_movie in raw_movie_list[1:]:
        movie = (
            raw_movie.split("&")[0]
            .split('">')[-1]
            .upper()
            .split(",")[0]
            .split(":")[0]
            .split(".")[0]
        )
        if movie in movies:
            movies[movie] += 1
        else:
            movies[movie] = 1
    print(movies)
    driver.close()
    return movies


def scrapp_cinemark_schedules(
    cinema_link: str = CINEMARK_PORTAL_NUNOA_URL, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    time.sleep(5)
    page = driver.page_source
    raw_movie_list = page.split("movie-schedule")
    for raw_movie in raw_movie_list[1:]:
        movie = (
            raw_movie.split('</a> <div class="movie-details">')[0]
            .split('">')[-1]
            .upper()
            .split(",")[0]
            .split(":")[0]
            .split(".")[0]
        )
        showings = raw_movie.count('<a class="btn btn-buy">')
        if movie in movies:
            movies[movie] += showings
        else:
            movies[movie] = showings
    print(movies)
    driver.close()
    return movies


def scrapp_every_cinema() -> Dict[str, str]:
    movies = {}
    for cinema_url in MAIN_CINEPOLIS_CINEMAS:
        movies = scrapp_cinehoyts_schedules(cinema_url, movies)
    for cinema_url in MAIN_CINEMARK_CINEMAS:
        movies = scrapp_cinemark_schedules(cinema_url, movies)
    print(movies)
    return movies
