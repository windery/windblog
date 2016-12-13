from flask import render_template, url_for, current_app, flash, redirect
from . import blog
from .forms import PostForm
from ..models import BlogPost
from .. import db
from config import Config

import time


def render_blog_template(template_name, **kwargs):
    return render_template(template_name, subjects=Config.SUBJECTS, **kwargs)


@blog.route('/')
@blog.route('/home')
def index():
    return render_blog_template('index.html')


@blog.route('/technique', methods=['GET'])
def technique():
    posts = []
    return render_blog_template('posts.html', posts=posts)


@blog.route('/environment', methods=['GET'])
def environment():
    posts = []
    return render_blog_template('posts.html', posts=posts)


@blog.route('/resources', methods=['GET'])
def resources():
    posts = []
    return render_blog_template('posts.html', posts=posts)


@blog.route('/thoughts', methods=['GET'])
def thoughts():
    posts = []
    return render_blog_template('posts.html', posts=posts)



@blog.route('/about', methods=['GET'])
def about():
    return render_blog_template('about.html')


@blog.route('/edit', methods=['Get', 'POST'])
def edit():
    post_form = PostForm()
    if post_form.validate_on_submit():
        blog_post = BlogPost(
            title = post_form.title.data,
            subject = post_form.subject.data,
            content = post_form.content.data,
            tags = post_form.tags.data,
            create_time = int(time.time()),
            modify_time = int(time.time())
        )
        print('title : ' + post_form.title.data)
        print('subject : ' + post_form.subject.data)
        print('content : ' + post_form.content.data)
        print('tags : ' + post_form.tags.data)
        db.session.add(blog_post)
        db.session.commit()
        print("success ----------------------------------------------------")
    return render_blog_template('edit.html', post_form=post_form)

