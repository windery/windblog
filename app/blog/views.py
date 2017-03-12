from datetime import datetime

from flask import render_template, url_for, flash, redirect, jsonify, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.blog.models import Post, Tag
from . import blog_blueprint as blog
from .forms import PostForm
from .. import db


@blog.route('/')
@blog.route('/home')
@blog.route('/index')
@blog.route('/index/<page>')
def index(page=1):
    if isinstance(page, str):
        page = int(page)
    pagination = Post.get_pagination(page)
    posts = pagination.items
    tags = Tag.get_tags()
    return render_template('blog/index.html', posts=posts, pagination=pagination, tags=tags)


@blog.route('/posts/<subject>')
@blog.route('/posts/<subject>/<page>')
def posts(subject=None, page=1):
    if isinstance(page, str):
        page = int(page)
    pagination = Post.get_pagination_by_subject(subject=subject, page=page)
    posts = pagination.items
    return render_template('blog/posts.html', posts=posts, pagination=pagination, subject=subject)


@blog.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@login_required
@blog.route('/edit', methods=['GET', 'POST'])
@blog.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title=None):
    post = None
    if title:
        post = Post.query.filter_by(title=title).first()
    post_form = PostForm()
    if post:
        if request.method == 'GET':
            post_form.title.data = post.title
            post_form.subject.data = post.subject_name
            post_form.content.data = post.content
            post_form.tags.data = post.tags
        post_form.update = True
    if post_form.validate_on_submit():
        title = post_form.title.data
        tags = post_form.tags.data
        if not post:
            post = Post(
                title=post_form.title.data,
                subject_name=post_form.subject.data,
                content=post_form.content.data,
                tags=post_form.tags.data,
                create_time=datetime.utcnow(),
                modify_time=datetime.utcnow()
            )
            db.session.add(post)
            flash('New post 【' + title + '】 successfully published', 'success')
        else:
            post.title=post_form.title.data
            post.subject_name=post_form.subject.data
            post.content=post_form.content.data
            post.tags=post_form.tags.data
            post.modify_time=datetime.utcnow()
            flash('Post【' + title + '】 sucessfully updated', 'success')
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        Tag.update_tags(title, tags)
        return redirect(url_for('.post', title=title))
    elif request.method is 'POST':
        flash('Some data not valid, fix them and try again', 'warning')
    return render_template('blog/edit.html', post_form=post_form, title=title)


@blog.route('/post/<title>', methods=['GET'])
def post(title):
    post = Post.query.filter_by(title=title).first()
    return render_template('blog/post.html', post=post)


@blog.route('/tag/<tag>', methods=['GET'])
def tag(tag):
    posts = []
    tag_records = Tag.query.filter_by(tag=tag).all()
    post_titles = [tag_record.post_title for tag_record in tag_records]
    for post_title in post_titles:
        post = Post.query.filter_by(title=post_title).first()
        if post:
            posts.append(post)
    return render_template('blog/tag.html', posts=posts, tag=tag)


@login_required
@blog.route('/delete/<title>')
def delete(title):
    post = Post.get_post_by_title(title)
    subject = post.subject_name
    Post.delete_post_by_title(title)
    flash('Post【' + title + '】 successfully deleted', 'success')
    return redirect(url_for('blog.'+subject))


@blog.route('/init')
def init():
    # init db
    json = {
        'code': 0,
        'message': 'Init windblog success'
    }

    from app.blog.models import Subject
    Subject.insert_subjects_if_not_exists()
    from app.user.models import User

    try:
        User.insert_administrator_in_not_exists()
    except AttributeError as e:
        json = {
            'code': -1,
            'message': 'Init administrator failed, message: %s' % e
        }
    return jsonify(json)

