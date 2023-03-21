import flask
import os
from dotenv import load_dotenv, find_dotenv


app = flask.Flask(__name__)
load_dotenv()  # load .env for API
app.secret_key = os.getenv("APP_SECRET_KEY")


@app.route("/")
def index():
    return flask.render_template("index.html")


app.run(debug=True)
