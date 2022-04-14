import time
from typing import Dict, List, Tuple

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CINEMARK_PORTAL_NUNOA_URL
from apps.cinema.models import Cinema
from apps.cinema.utils import save_movie_and_schedule


def _get_raw_movie_list(page: str) -> List[str]:
    return page.split("PREVENTAS")[0].split("movie-schedule")


def _get_movie(raw_movie: str) -> str:
    return (
        raw_movie.split('</a> <div class="movie-details">')[0].split('">')[-1].upper()
    )


def _get_schedules(raw_movie: str) -> List[str]:
    return raw_movie.split('<a class="btn btn-buy">')[1:]


def _get_schedule(raw_schedule: str) -> str:
    return raw_schedule.split("</a></div>")[0].split("</a>")[0]


def scrapp_schedules(cinema_link: str = CINEMARK_PORTAL_NUNOA_URL) -> None:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    time.sleep(5)
    page = driver.page_source
    raw_movie_list = _get_raw_movie_list(page)
    for raw_movie in raw_movie_list[1:]:
        movie = _get_movie(raw_movie)
        raw_schedules = _get_schedules(raw_movie)
        for raw_schedule in raw_schedules:
            current_cinema = Cinema.objects.get(link=cinema_link)
            schedule = _get_schedule(raw_schedule)
            save_movie_and_schedule(movie, current_cinema, schedule)
    driver.close()
