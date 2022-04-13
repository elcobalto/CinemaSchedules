from bs4 import BeautifulSoup
import requests

CINEPOLIS_LA_REINA_URL = 'https://cinehoyts.cl/cartelera/santiago-oriente/cinepolis-la-reina'
CINEMARK_ALTO_LAS_CONDES_URL = 'https://www.cinemark.cl/cine?tag=2300&cine=cinemark_portal_nunoa'

def scrapp_cinehoyts_schedule(hoyts_link: str = CINEPOLIS_LA_REINA_URL):
    page = requests.get(hoyts_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)

def scrapp_cinemark_schedule(hoyts_link: str = CINEMARK_ALTO_LAS_CONDES_URL):
    page = requests.get(hoyts_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
