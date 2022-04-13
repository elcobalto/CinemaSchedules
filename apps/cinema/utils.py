from difflib import SequenceMatcher
from typing import Dict, Tuple


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def clean_movie_title(movie: str) -> str:
    return movie.replace("PELICULA", "").replace("MOVIE", "")


def similar_movies(movie: str, possible_movie: str) -> bool:
    clean_movie = clean_movie_title(movie)
    clan_possible = clean_movie_title(possible_movie)
    similarity = similar(clean_movie, clan_possible)
    is_substring = (
        clean_movie in clan_possible
        if len(clean_movie) < len(clan_possible)
        else clan_possible in clean_movie
    )
    if not is_substring:
        similarity = similar(clean_movie, clan_possible)
    return is_substring or similarity > 0.5


def movie_exists(movie: str, movies: Dict[str, str]) -> Tuple[bool, str]:
    for possible in movies.keys():
        if similar_movies(movie, possible):
            return True, possible
    return False, movie
