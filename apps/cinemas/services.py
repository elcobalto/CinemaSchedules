from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

CINEPOLIS_LA_REINA_URL = (
    "https://cinehoyts.cl/cartelera/santiago-oriente/cinepolis-la-reina"
)
CINEMARK_ALTO_LAS_CONDES_URL = (
    "https://www.cinemark.cl/cine?tag=2300&cine=cinemark_portal_nunoa"
)


def scrapp_cinehoyts_schedule(hoyts_link: str = CINEPOLIS_LA_REINA_URL):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(hoyts_link)
    page = driver.page_source
    raw_movie_list = page.split("originalTitle=")
    movies = {}
    for raw_movie in raw_movie_list[1:]:
        movie = raw_movie.split("&")[0]
        if movie in movies:
            movies[movie] += 1
        else:
            movies[movie] = 1
    print(movies)
    driver.close()

