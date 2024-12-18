from flask import Blueprint

bp = Blueprint("verification", __name__)

from app.verification import routes
