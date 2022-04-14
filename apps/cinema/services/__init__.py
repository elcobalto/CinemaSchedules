from apps.cinema.constants import MAIN_CINEMARK_CINEMAS, MAIN_CINEPOLIS_CINEMAS
from apps.cinema.models import Cinema
from apps.cinema.services.biografo import scrapper as biografo_scrapper
from apps.cinema.services.centro_arte_alameda import \
    scrapper as alameda_scrapper
from apps.cinema.services.cinehoyts import scrapper as cinehoyts_scrapper
from apps.cinema.services.cinemark import scrapper as cinemark_scrapper
from apps.cinema.services.normandie import scrapper as normandie_scrapper


def scrapp_every_cinema():
    biografo_scrapper.scrapp_schedules()
    # alameda_scrapper.scrapp_schedules()
    for cinema_url in MAIN_CINEPOLIS_CINEMAS:
        cinema = Cinema.objects.get(link=cinema_url)
        cinehoyts_scrapper.scrapp_schedules(cinema)
    for cinema_url in MAIN_CINEMARK_CINEMAS:
        cinemark_scrapper.scrapp_schedules(cinema_url)
    normandie_scrapper.scrapp_schedules()
