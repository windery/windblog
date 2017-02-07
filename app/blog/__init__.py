#!venv/bin/python3
# -*- coding:utf8 -*-

from flask import Blueprint

blog_blueprint = Blueprint('blog', __name__)

from . import errors, views, models, forms
