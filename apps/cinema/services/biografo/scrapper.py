from typing import Dict, List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import EL_BIOGRAFO
from apps.cinema.models import Cinema, Schedule
from apps.cinema.utils import save_movie_and_schedule


def _get_raw_movie_list(page: str) -> List[str]:
    return page.split('rel="bookmark">')


def _get_movie(raw_movie: str) -> str:
    return raw_movie.split("</a>")[0][:-10].upper()


def _get_schedule(raw_movie: str) -> str:
    return raw_movie.split("</a>")[0][-9:-4]


def scrapp_schedules(cinema_link: str = EL_BIOGRAFO) -> None:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = _get_raw_movie_list(page)
    for raw_movie in raw_movie_list[1:]:
        movie = _get_movie(raw_movie)
        current_cinema = Cinema.objects.get(link=cinema_link)
        schedule = _get_schedule(raw_movie)
        save_movie_and_schedule(movie, current_cinema, schedule)
    driver.close()
