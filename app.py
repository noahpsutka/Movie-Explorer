import flask
import requests
import random
import os
from dotenv import load_dotenv, find_dotenv


app = flask.Flask(__name__)
load_dotenv(find_dotenv())  # load .env for API
app.secret_key = os.getenv("APP_SECRET_KEY")
MOV_API_BASE_URL = "https://api.themoviedb.org/3/"
MOV_API_QUERY_PATH = "discover/movie"


@app.route("/")
def index():
    movie_title = get_trending_movie()
    return flask.render_template("index.html", name=movie_title)


def get_trending_movie():
    mov_response = requests.get(
        MOV_API_BASE_URL + MOV_API_QUERY_PATH,
        params={
            "api_key": os.getenv("TMDB_API_KEY"),
        },
    )
    movies_list = mov_response.json()["results"]
    return movies_list[random.randint(0, 10)]["title"]


app.run(debug=True)
