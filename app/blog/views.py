from flask import render_template, url_for, flash, redirect, jsonify
from . import blog
from .forms import PostForm
from ..models import Post, Subject
from .. import db
from config import Config
from datetime import datetime


def render_blog_template(template_name, **kwargs):
    return render_template(template_name, subjects=Config.SUBJECTS, **kwargs)

def get_posts_by_subject(subject_name):
    return Post.query.filter_by(subject_name=subject_name).all()

def get_all_posts():
    return Post.query.all()


@blog.route('/')
@blog.route('/home')
def index():
    posts = get_all_posts()
    return render_blog_template('index.html', posts=posts)


@blog.route('/technique', methods=['GET'])
def technique():
    posts = get_posts_by_subject(subject_name='technique')
    return render_blog_template('posts.html', posts=posts)


@blog.route('/environment', methods=['GET'])
def environment():
    posts = get_posts_by_subject(subject_name='environment')
    return render_blog_template('posts.html', posts=posts)


@blog.route('/resources', methods=['GET'])
def resources():
    posts = get_posts_by_subject(subject_name='resources')
    return render_blog_template('posts.html', posts=posts)


@blog.route('/thoughts', methods=['GET'])
def thoughts():
    posts = get_posts_by_subject(subject_name='thoughts')
    return render_blog_template('posts.html', posts=posts)



@blog.route('/about', methods=['GET'])
def about():
    return render_blog_template('about.html')


@blog.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    if title:
        post = Post.query.filter_by(title=title).first()
    post_form = PostForm()
    if post:
        post_form.title.data = post.title
        post_form.subject.data = post.subject_name
        post_form.content.data = post.content
        post_form.tags.data = post.tags
        post_form.update = True
    if post_form.validate_on_submit():
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
            flash('new post ' + post_form.title.data + ' has been published')
        else:
            post.title=post_form.title.data,
            post.subject_name=post_form.subject.data,
            post.content=post_form.content.data,
            post.tags=post_form.tags.data,
            post.create_time=datetime.utcnow(),
            post.modify_time=datetime.utcnow()
            flash('post ' + post_form.title.data + ' has been updated')
        db.session.commit()
    return render_blog_template('edit.html', post_form=post_form)


@blog.route('/post/<title>', methods=['GET'])
def post(title):
    post = Post.query.filter_by(title=title).first()
    return render_blog_template('post.html', post=post)


@blog.route('/init_db', methods=['GET'])
def init_db():
    Subject.insert_subjects()
    json = {
        'code': 0,
        'message': "init subjects in db success"
    }
    return jsonify(json)

