from datetime import datetime
from typing import Dict, List, Tuple

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from apps.cinema.constants import CENTRO_ARTE_ALAMEDA
from apps.cinema.models import Cinema
from apps.cinema.utils import save_movie_and_schedule


def _get_raw_movie_list(page: str) -> List[str]:
    return (
        page.split("La CARTELERA PRESENCIAL de esta semana en Centro Arte Alameda")[1]
        .split("Te esperamos en Centro Arte Alameda")[0]
        .split("🎬 ")
    )


def _get_movie(raw_movie: str) -> str:
    return raw_movie.split(" (")[0].upper()


def _get_schedules(raw_movie: str) -> List[str]:
    return raw_movie.split("\n")[1:-1]


def _get_schedule(raw_schedule: str) -> Tuple[str, List]:
    raw_schedule_info = raw_schedule.split(" ")
    return raw_schedule_info[3], raw_schedule_info[1].split("/")


def scrapp_schedules(cinema_link: str = CENTRO_ARTE_ALAMEDA) -> None:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(cinema_link)
    page = driver.page_source
    raw_movie_list = _get_raw_movie_list(page)
    for raw_movie in raw_movie_list[1:]:
        movie = _get_movie(raw_movie)
        current_cinema = Cinema.objects.get(link=cinema_link)
        schedules = _get_schedules(raw_movie)
        for raw_schedule in schedules:
            schedule, raw_week = _get_schedule(raw_schedule)
            today = datetime.today()
            week = datetime.date(int(today.year), int(raw_week[1]), int(raw_week[0]))
            save_movie_and_schedule(movie, current_cinema, schedule, week)
    driver.close()
