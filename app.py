import flask
import requests
import random
import os
from dotenv import load_dotenv, find_dotenv


app = flask.Flask(__name__)
load_dotenv(find_dotenv())  # load .env for API
app.secret_key = os.getenv("APP_SECRET_KEY")


@app.route("/")
def index():
    random_movie = movie_id_list[random.randint(0, 4)]
    movie_title = get_movie_info(random_movie, "title")
    movie_tagline = get_movie_info(random_movie, "tagline")
    movie_overview = get_movie_info(random_movie, "overview")
    movie_score = get_movie_info(random_movie, "vote_average")
    movie_genre = get_movie_genre(random_movie, "genres")
    movie_link = get_image(random_movie)
    movie_image = "https://image.tmdb.org/t/p/w500/" + movie_link
    wiki_id = get_wiki(movie_title)
    wiki_link = " https://en.wikipedia.org/?curid=" + str(wiki_id)
    return flask.render_template(
        "index.html",
        title=movie_title,
        image=movie_image,
        tag=movie_tagline,
        genre=movie_genre,
        overview=movie_overview,
        score=round(movie_score, 1),
        wiki=wiki_link,
    )


MOV_API_BASE_URL = "https://api.themoviedb.org/3/"
MOV_API_MOVIE_PATH = "movie/"
MOV_API_IMAGE_PATH = "/images"
movie_id_list = ["808", "585", "238", "205321", "634649"]


def get_movie_info(random_movie, request):
    mov_response = requests.get(
        MOV_API_BASE_URL + MOV_API_MOVIE_PATH + random_movie,
        params={
            "api_key": os.getenv("TMDB_API_KEY"),
        },
    )
    movie_info = mov_response.json()[request]
    return movie_info


def get_movie_genre(random_movie, request):
    mov_response = requests.get(
        MOV_API_BASE_URL + MOV_API_MOVIE_PATH + random_movie,
        params={
            "api_key": os.getenv("TMDB_API_KEY"),
        },
    )
    movie_info = mov_response.json()[request]
    genres = ""
    for genre in movie_info:
        genres = genres + genre["name"] + " "
    return genres


def get_image(random_movie):
    mov_response = requests.get(
        MOV_API_BASE_URL + MOV_API_MOVIE_PATH + random_movie + MOV_API_IMAGE_PATH,
        params={
            "api_key": os.getenv("TMDB_API_KEY"),
        },
    )
    movie_image = mov_response.json()["posters"][0]["file_path"]
    return movie_image


WIKI_API_BASE_URL = "https://en.wikipedia.org/w/api.php"


def get_wiki(movie_title):
    wiki_response = requests.get(
        WIKI_API_BASE_URL,
        params={
            "action": "query",
            "format": "json",
            "titles": movie_title,
            "formatversion": "2",
        },
    )
    wiki_info = wiki_response.json()["query"]["pages"][0]["pageid"]
    return wiki_info
