from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/')

from .import routes, models