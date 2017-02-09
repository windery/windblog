from datetime import datetime

from flask import render_template, url_for, flash, redirect, jsonify, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app.blog.models import Post, Subject, Tag
from . import blog_blueprint as blog
from .forms import PostForm
from .. import db


@blog.route('/')
@blog.route('/home')
@blog.route('/index')
def index():
    posts = Post.get_latest_posts()
    tags = Tag.get_tags()
    return render_template('blog/index.html', posts=posts, tags=tags)


@blog.route('/technique', methods=['GET'])
def technique():
    posts = Post.get_latest_posts_by_subject(subject_name='technique')
    return render_template('blog/posts.html', posts=posts, subject='technique')


@blog.route('/environment', methods=['GET'])
def environment():
    posts = Post.get_latest_posts_by_subject(subject_name='environment')
    return render_template('blog/posts.html', posts=posts, subject='environment')


@blog.route('/resources', methods=['GET'])
def resources():
    posts = Post.get_latest_posts_by_subject(subject_name='resources')
    return render_template('blog/posts.html', posts=posts, subject='resources')


@blog.route('/thoughts', methods=['GET'])
def thoughts():
    posts = Post.get_latest_posts_by_subject(subject_name='thoughts')
    return render_template('blog/posts.html', posts=posts, subject='thoughts')


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
@blog.route('/init_db', methods=['GET'])
def init_db():
    Subject.insert_subjects()
    json = {
        'code': 0,
        'message': "Init subjects in db success"
    }
    return jsonify(json)


@login_required
@blog.route('/clear_db', methods=['GET'])
def clear_db():
    Post.clear()
    Subject.clear()
    json = {
        'code': 0,
        'message': 'Clear subjects in db success'
    }
    return jsonify(json)


@login_required
@blog.route('/delete/<title>')
def delete(title):
    post = Post.get_post_by_title(title)
    subject = post.subject_name
    Post.delete_post_by_title(title)
    flash('Post【' + title + '】 successfully deleted', 'success')
    return redirect(url_for('blog.'+subject))

