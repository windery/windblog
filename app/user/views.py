from . import user_blueprint as user
from app.blog.models import Post
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm
from .models import User


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username='admin').first()
        if user is None:
            flash('Please initialize your app first, and make sure password configuration is ok!', 'danger')
        elif user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('user.admin'))
        else:
            flash('Invalid username or password.', "warning")
    return render_template('user/login.html', form=form)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category="success")
    return redirect(url_for('blog.index'))


@login_required
@user.route('/admin', methods=['GET'])
def admin():
    return render_template('user/admin.html')


@login_required
@user.route('/manage/<target>', methods=['GET'])
def manage(target=None):
    if target == 'blog':
        posts = Post.get_latest_posts()
        return render_template('user/manage_posts.html', posts=posts)
    elif target == 'file':
        return render_template('user/manage_files.html')
    else:
        flash('no concrete management specified', 'warning')
        return redirect(url_for('user.admin'))


