from typing import Any, Dict, List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CINEPOLIS_LA_REINA_URL
from apps.cinema.models import Cinema, Showing
from apps.cinema.utils import save_movie_and_schedule

CINEPOLIS_LA_REINA = Cinema.objects.get(link=CINEPOLIS_LA_REINA_URL)


def _get_raw_movie_list(page: str) -> List[str]:
    return page.split("originalTitle=")


def _get_cinema(raw_movie: str, previous_cinema: str) -> str:
    try:
        return raw_movie.split('data-list="')[1].split('" data-moviekey="')[0]
    except IndexError:
        return previous_cinema


def _get_movie(raw_movie: str) -> str:
    return raw_movie.split("&")[0].split('">')[-1].upper()


def _get_schedule(raw_movie: str) -> str:
    return raw_movie.split("</a>")[0].split('="ng-binding">')[-1]


def scrapp_schedules(cinema: Cinema = CINEPOLIS_LA_REINA) -> None:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema.link)
    page = driver.page_source
    raw_movie_list = _get_raw_movie_list(page)
    next_cinema_keyword = _get_cinema(raw_movie_list[0], "")
    for raw_movie in raw_movie_list[1:]:
        movie = _get_movie(raw_movie)
        print(next_cinema_keyword)
        current_cinema = Cinema.objects.get(keyword=next_cinema_keyword)
        schedule = _get_schedule(raw_movie)
        save_movie_and_schedule(movie, current_cinema, schedule)
        next_cinema_keyword = _get_cinema(raw_movie, next_cinema_keyword)
    driver.close()
