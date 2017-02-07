from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

from . import models, views, errors
