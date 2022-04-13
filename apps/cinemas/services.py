from bs4 import BeautifulSoup
import requests

HOYTS_LA_REINA_URL = 'https://cinehoyts.cl/cartelera/santiago-oriente/cinepolis-la-reina'

def scrapp_cinehoyts_schedule(hoyts_link: str = HOYTS_LA_REINA_URL):
    page = requests.get(hoyts_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
