from flask import Blueprint
from app.controllers import anime_stock_controller

bp = Blueprint("anime_stock", __name__, url_prefix="/animes")

bp.post("")(anime_stock_controller.create_anime)
bp.get("")(anime_stock_controller.get_animes)
bp.get("/<anime_id>")(anime_stock_controller.get_anime_by_id)
bp.patch("/<anime_id>")(anime_stock_controller.patch_anime)
bp.delete("/<anime_id>")(anime_stock_controller.delete_anime)