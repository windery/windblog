#!venv/bin/python3
# -*- coding:utf8 -*-

from flask import render_template
from . import blog

@blog.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@blog.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@blog.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
