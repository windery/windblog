from flask import render_template, url_for, current_app, flash, redirect
from . import blog
from .. import db

def render_blog_template(template_name, **kwargs):
    subjects = (
        (u'主页','/home'),
        (u'技术', '/technique'),
        (u'环境', '/environment'),
        (u'资源', '/resources'),
        (u'思考', '/thoughts'),
        (u'关于', '/about')
    )
    return render_template(template_name, subjects=subjects, **kwargs)

@blog.route('/')
@blog.route('/home')
def index():
    return render_blog_template('index.html')

@blog.route('/technique', methods=['GET'])
def technique():
    return render_blog_template('posts.html')

@blog.route('/environment', methods=['GET'])
def environment():
    return render_blog_template('posts.html')

@blog.route('/resources', methods=['GET'])
def resources():
    return render_blog_template('posts.html')

@blog.route('/thoughts', methods=['GET'])
def thoughts():
    return render_blog_template('posts.html')

@blog.route('/about', methods=['GET'])
def about():
    return render_blog_template('about.html')

