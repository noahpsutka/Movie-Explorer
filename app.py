import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy  # SQL Database
import flask_login
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # load .env for API

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.secret_key = os.getenv("APP_SECRET_KEY")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    random_movie = movie_id_list[random.randint(0, 4)]
    return flask.redirect(flask.url_for("display_movie", id=random_movie))


@app.route("/movie")
def display_movie():
    random_movie = request.args["id"]
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


@app.route("/login", methods=["GET"])
def handle_login():
    return flask.render_template("login.html")


@app.route("/signup", methods=["GET"])
def handle_signup():
    return flask.render_template("signup.html")


@app.route("/logout")
@flask_login.login_required
def handle_logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/login", methods=["POST"])
def user_login():
    form_data = flask.request.form
    user_name = form_data["user_name"]
    user_password = form_data["user_password"]
    user = User.query.filter_by(username=user_name).first()
    if not user or not check_password_hash(user.password, user_password):
        flask.flash(
            "Login Error: Username or password is invalid. Please try logging in again, or create an account."
        )
        return flask.redirect(flask.url_for("user_login"))
    else:
        # if valid user, user is now logged in
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("index"))


@app.route("/signup", methods=["POST"])
def user_signup():
    form_data = flask.request.form
    user_name = form_data["user_name"]
    user_password = form_data["user_password"]
    user = User.query.filter_by(username=user_name).first()
    if user:
        flask.flash("Error in Account Creation: Username is taken. Please try again.")
        return flask.redirect(flask.url_for("user_signup"))
    else:
        new_user = User(
            username=user_name,
            password=generate_password_hash(user_password, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        flask.flash("Successfully signed up")
        return flask.redirect(flask.url_for("user_login"))


MOV_API_BASE_URL = "https://api.themoviedb.org/3/"
MOV_API_MOVIE_PATH = "movie/"
MOV_API_IMAGE_PATH = "/images"
movie_id_list = ["808", "585", "238", "205321", "634649"]
# [Shrek: 808, Monsters Inc: 585, Godfather: 238, Sharknado: 205321, Spiderman No Way Home: 634649 ]


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
