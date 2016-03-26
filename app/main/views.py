from flask import render_template, url_for, current_app, flash, redirect
from flask.ext.login import login_required, current_user, login_user
from . import main
from .. import db
from ..models import User
from .forms import RegisterForm, LoginForm

@main.route('/')
def index(username=None):
    if username is None:
        username = 'Stranger'
    return render_template('index.html', username=username)

@main.route('/user/<username>')
@login_required
def user(username=None):
    if current_user.username == username:
        return render_template('user.html', username=username)
    else:
        return render_template(url_for('main.login'))

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

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登陆成功！')
            return redirect(url_for('main.user', username=user.username))
        else:
            flash('登陆失败，邮箱或密码有误!')
    return render_template('login.html', form=form)

