from flask import render_template, url_for, current_app, flash, redirect
from . import main
from .. import db
from ..models import User
from .forms import RegisterForm

@main.route('/')
@main.route('/user/<username>')
def index(username=None):
    if username is not None:
        user = User.query.filter_by(username=username).first_or_404()
        username = user.username
    else:
        username = 'Stranger'
    return render_template('index.html', username=username)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    username=form.username.data,
                    password=form.password.data,
                    sex=form.sex.data,
                    age=form.age.data,
                    about_me=form.about_me.data)
        db.session.add(user)
        db.session.commit()
        flash('Regestration completed. Now login in with the account you just registed.')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

