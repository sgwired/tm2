from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.errors import handlers