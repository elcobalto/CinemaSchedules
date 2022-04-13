from typing import Dict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import EL_BIOGRAFO
from apps.cinema.utils import movie_exists


def scrapp_schedules(
    cinema_link: str = EL_BIOGRAFO, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = page.split('rel="bookmark">')
    for raw_movie in raw_movie_list[1:]:
        movie = raw_movie.split("</a>")[0][:-10].upper()
        does_exists, movie_key = movie_exists(movie, movies)
        if not does_exists:
            movies[movie_key] = 1
    print(movies)
    driver.close()
    return movies
