from flask import render_template, url_for, current_app, flash, redirect
from . import blog
from .forms import PostForm
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

@blog.route('/edit', methods=['GET', 'POST'])
def edit():
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        subject = post_form.subject.data
        content = post_form.content.data
        tags = post_form.tags.data
        print('title:', title)
        print('subject:', subject)
        print('content:', content)
        print('tags:', tags)
    return render_blog_template('edit.html', post_form=post_form)

