from typing import Dict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CINEPLANET
from apps.cinema.utils import movie_exists


def scrapp_schedules(
    cinema_link: str = CINEPLANET, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(f"{cinema_link}/la-medium")
    page = driver.page_source
    raw_movie_list = page.split("movie-schedule")
    for raw_movie in raw_movie_list[1:]:
        movie = (
            raw_movie.split('</a> <div class="movie-details">')[0]
            .split('">')[-1]
            .upper()
        )
        showings = raw_movie.count('<a class="btn btn-buy">')
        does_exists, movie_key = movie_exists(movie, movies)
        if does_exists:
            movies[movie_key] += showings
        else:
            movies[movie_key] = showings
    print(movies)
    driver.close()
    return movies
