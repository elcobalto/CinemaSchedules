from typing import Dict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CINE_ARTE_NORMANDIE
from apps.cinema.utils import movie_exists


def scrapp_schedules(
    cinema_link: str = CINE_ARTE_NORMANDIE, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = page.split('<div class="contenedorcartelera">')[1].split(
        "<strong>"
    )
    for raw_movie in raw_movie_list[1:]:
        movie = (
            raw_movie.split("</strong>")[0].split("</br>")[0].split("<br>")[0].upper()
        )
        does_exists, movie_key = movie_exists(movie, movies)
        if not does_exists:
            movies[movie_key] = 1
    print(movies)
    driver.close()
    return movies
