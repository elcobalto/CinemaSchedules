from typing import Dict, List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CINE_ARTE_NORMANDIE
from apps.cinema.models import Cinema
from apps.cinema.utils import save_movie_and_schedule


def _get_raw_movie_list(page: str) -> List[str]:
    return page.split('<div class="contenedorcartelera">')[1].split("<strong>")


def _get_movie(raw_movie: str) -> str:
    return (
        raw_movie.split("</strong>")[0]
        .split("</br>")[0]
        .split("<br>")[0]
        .split("&NBSP;")[0]
        .split("(")[0]
        .rstrip()
        .upper()
    )


def _get_schedule(raw_movie: str) -> str:
    return raw_movie.split(" hrs.")[0][-5:]


def scrapp_schedules(
    cinema_link: str = CINE_ARTE_NORMANDIE, movies: Dict[str, str] = {}
) -> Dict[str, str]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = _get_raw_movie_list(page)
    for raw_movie in raw_movie_list[1:]:
        movie = _get_movie(raw_movie)
        if movie == "SIN FUNCIONES DE CINE":
            continue
        current_cinema = Cinema.objects.get(link=cinema_link)
        schedule = _get_schedule(raw_movie)
        save_movie_and_schedule(movie, current_cinema, schedule)
    driver.close()
