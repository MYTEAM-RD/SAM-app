from flask import Blueprint

bp = Blueprint("analyse", __name__)

from app.analyse import routes
