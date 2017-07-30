from datetime import datetime

from flask import render_template, url_for, flash, redirect, jsonify, request, current_app as blog_app
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

import mistune

from app.blog.models import Post, Tag
from ..utils.log_util import log_request
from . import blog_blueprint as blog
from .forms import PostForm
from .. import db


@blog.route('/')
@blog.route('/index')
@blog.route('/index/<int:page>')
def index(page=1):
    log_request('access index page[%d]' % page)
    pagination = Post.get_pagination(page)
    posts = pagination.items
    tags = Tag.get_tags()
    return render_template('blog/index.html', posts=posts, pagination=pagination, tags=tags)


@blog.route('/posts/<subject>')
@blog.route('/posts/<subject>/<int:page>')
def posts(subject=None, page=1):
    log_request('access posts with subject[%s] page[%d]' % (subject or '', page))
    pagination = Post.get_pagination_by_subject(subject=subject, page=page)
    posts = pagination.items
    return render_template('blog/posts.html', posts=posts, pagination=pagination, subject=subject)


@blog.route('/about', methods=['GET'])
def about():
    log_request('access about page')
    blog_app.logger.info(request.method + ' ' + request.remote_addr + ' accessed ' + request.path )
    return render_template('about.html')


@login_required
@blog.route('/edit', methods=['GET', 'POST'])
@blog.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title=None):
    post = None
    if title:
        log_request('access edit post[%s] page' % title)
        post = Post.query.filter_by(title=title).first()
    else:
        log_request('access create new post page')
    post_form = PostForm()
    if post:
        if request.method == 'GET':
            post_form.title.data = post.title
            post_form.subject.data = post.subject_name
            post_form.content.data = post.content
            post_form.tags.data = post.tags
        post_form.update = True
        blog_app.logger.info('post[%s] original data is [%s]' % (post.title, post_form.to_json()))
    if post_form.validate_on_submit():
        blog_app.logger.info('after edit post[%s], current data is [%s]' % (title, post_form.to_json()))
        title = post_form.title.data
        tags = post_form.tags.data
        if not post:
            content = post_form.content.data
            content_md = mistune.markdown(content)
            brief_content = content[0:100]
            brief_content_md = mistune.markdown(brief_content)
            post = Post(
                title=post_form.title.data,
                subject_name=post_form.subject.data,
                content=content,
                content_md=content_md,
                brief_content=brief_content,
                brief_content_md=brief_content_md,
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
        except IntegrityError as e:
            db.session.rollback()
            blog_app.logger.error('db error when adding post[%s], message : %s' % (title, e))
        Tag.update_tags(title, tags)
        return redirect(url_for('.post', title=title))
    elif request.method is 'POST':
        flash('Some data not valid, fix them and try again', 'warning')
        blog_app.logger.warning('some data not valid in post [%s]' % title)
    return render_template('blog/edit.html', post_form=post_form, title=title)


@blog.route('/post/<title>', methods=['GET', 'POST'])
def post(title):
    log_request('access post page with title[%s]' % title)
    post = Post.query.filter_by(title=title).first()
    if not post:
        blog_app.logger.warning('post[%s] not exists' % title)
        flash('post[%s] not exists' % title)
        return redirect(url_for('blog.index'))
    blog_app.logger.info('get post with title[%s] success' % title)
    return render_template('blog/post.html', post=post)


@blog.route('/tag/<tag>', methods=['GET'])
@blog.route('/tag/<tag>/<int:page>')
def tag(tag, page=1):
    log_request('access page with tag[%s] and page[%d]' % (tag, page))
    if isinstance(page, str):
        page = int(page)
    pagination = Post.get_pagination_by_tag(tag=tag, page=page)
    posts = pagination.items
    blog_app.logger.info('get posts with tag [%s] on page [%s] success' % (tag, page))
    return render_template('blog/tag.html', posts=posts, pagination=pagination, tag=tag)


@login_required
@blog.route('/delete/<title>')
def delete(title):
    log_request('delete post[%s]' % title)
    post = Post.get_post_by_title(title)
    subject = post.subject_name
    Post.delete_post_by_title(title)
    flash('Post【' + title + '】 successfully deleted', 'success')
    blog_app.logger.info('Post [' + title + '] successfully deleted')
    return redirect(request.values.get('next') or url_for('blog.posts', subject=subject))


@blog.route('/init')
def init():
    log_request('access init page')
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
        blog_app.logger.error('init app failed, message : ' + e)
    return jsonify(json)

