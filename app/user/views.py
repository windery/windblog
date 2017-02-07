from . import user_blueprint as user
from app import db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from .models import User


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('.profile'))
        flash('Invalid username or password.', "warning")
    return render_template('user/login.html', form=form)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category="success")
    return redirect(url_for('blog.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('You can login now.', category='success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)

@user.route('/profile', methods=['GET'])
def profile():
    return render_template('user/profile.html')
