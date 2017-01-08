from flask import render_template, url_for, flash, redirect, jsonify, request
from . import blog
from .forms import PostForm
from ..models import Post, Subject
from .. import db
from datetime import datetime


@blog.route('/')
@blog.route('/home')
@blog.route('/index')
def index():
    posts = Post.get_latest_posts()
    return render_template('index.html', posts=posts)


@blog.route('/manager', methods=['GET'])
def manager():
    return  render_template('manager.html')


@blog.route('/technique', methods=['GET'])
def technique():
    posts = Post.get_latest_posts_by_subject(subject_name='technique')
    return render_template('posts.html', posts=posts, subject='technique')


@blog.route('/environment', methods=['GET'])
def environment():
    posts = Post.get_latest_posts_by_subject(subject_name='environment')
    return render_template('posts.html', posts=posts, subject='environment')


@blog.route('/resources', methods=['GET'])
def resources():
    posts = Post.get_latest_posts_by_subject(subject_name='resources')
    return render_template('posts.html', posts=posts, subject='resources')


@blog.route('/thoughts', methods=['GET'])
def thoughts():
    posts = Post.get_latest_posts_by_subject(subject_name='thoughts')
    return render_template('posts.html', posts=posts, subject='thoughts')



@blog.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


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
            flash('new post 【' + title + '】 successfully published', 'success')
        else:
            post.title=post_form.title.data
            post.subject_name=post_form.subject.data
            post.content=post_form.content.data.strip()
            post.tags=post_form.tags.data
            post.modify_time=datetime.utcnow()
            flash('post【' + title + '】  has been updated', 'success')
        db.session.commit()
        return redirect(url_for('.post', title=title))
    elif request.method is 'POST':
        flash('some data not valid, fix them and try again', 'warning')
    return render_template('edit.html', post_form=post_form, title=title)


@blog.route('/post/<title>', methods=['GET'])
def post(title):
    post = Post.query.filter_by(title=title).first()
    return render_template('post.html', post=post)


@blog.route('/init_db', methods=['GET'])
def init_db():
    Subject.insert_subjects()
    json = {
        'code': 0,
        'message': "init subjects in db success"
    }
    return jsonify(json)

