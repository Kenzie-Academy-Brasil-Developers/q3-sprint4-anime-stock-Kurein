from flask import Flask, Blueprint
from app.routes.anime_stock_routes import bp as animes_bp

bp_api = Blueprint("api", __name__, url_prefix="")

def init_app(app: Flask):
    bp_api.register_blueprint(animes_bp)

    app.register_blueprint(bp_api)