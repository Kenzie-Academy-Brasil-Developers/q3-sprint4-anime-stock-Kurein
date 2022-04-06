from flask import Flask
from app import routes
from app.models.anime_model import Anime

def create_app():
    app = Flask(__name__)

    Anime().table_init()

    routes.init_app(app)

    return app