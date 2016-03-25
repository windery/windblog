from flask import render_template, url_for, current_app, flash
from . import main
from .. import db
from ..models import User

@main.route('/')
@main.route('/user/<username>')
def index(username=None):
    if username is not None:
        user = User.query.filter_by(username=username).first_or_404()
        username = user.username
    else:
        username = 'Stranger'
    return render_template('index.html', username=username)

