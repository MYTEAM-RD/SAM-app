from flask import Blueprint

cli = Blueprint("admin", __name__)

from app.admin import commands
