import os
from flask import render_template, redirect, url_for, request, flash, current_app as blog_app, send_from_directory, Response, stream_with_context
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from pathlib import Path
from requests import get

from . import user_blueprint as user
from app.blog.models import Post
from app.utils.log_util import log_request
from .forms import LoginForm, FileForm, DownloadProxyForm
from .models import User



@user.route('/login', methods=['GET', 'POST'])
def login():
    log_request('login administrator')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username='administrator').first()
        if user is None:
            flash('Please initialize your app first, and make sure password configuration is ok!', 'danger')
            blog_app.logger.warning('administrator not initialized, check configuration then init app')
        elif user.verify_password(form.password.data):
            login_user(user)
            blog_app.logger.info('administrator successfully logined')
            flash('login successfully', "success")
            return redirect(request.args.get('next') or url_for('user.admin'))
        else:
            flash('Invalid username or password.', "warning")
            blog_app.logger.warning('administrator password not right')
    return render_template('user/login.html', form=form)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    log_request('logout administrator')
    logout_user()
    flash('You have logged out.', category="success")
    blog_app.logger.info('administrator logout successfully')
    return redirect(url_for('blog.index'))


@login_required
@user.route('/admin', methods=['GET'])
def admin():
    log_request('access administrator page')
    return render_template('user/admin.html')


@login_required
@user.route('/manage/<target>', methods=['GET'])
def manage(target=None):
    if target == 'blog':
        posts = Post.get_latest_posts()
        blog_app.logger.info('accessed post manage page')
        return render_template('user/manage_posts.html', posts=posts)
    elif target == 'file':
        upload_folder = blog_app.config['WINDBLOG_UPLOAD_FOLDER']
        filenames = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
        blog_app.logger.info('accessed post manage page, filenames : %s' % filenames)
        return render_template('user/manage_files.html', filenames=filenames)
    else:
        flash('no concrete management specified', 'warning')
        blog_app.logger.warning('no management target specefied')
        return redirect(url_for('user.admin'))


@login_required
@user.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = FileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            blog_app.logger.debug('when uploading file, form data is %s' % (form.to_json()))
            file = form.file.data
            filename = secure_filename(file.filename)
            upload_folder = blog_app.config['WINDBLOG_UPLOAD_FOLDER']
            if not os.path.isdir(upload_folder):
                blog_app.logger.debug('upload dir [%s] not exists and will be created' % upload_folder)
                os.mkdir(upload_folder)
            blog_app.logger.debug('upload file[%s] to [%s]' % (filename, upload_folder))
            file.save(os.path.join(upload_folder, filename))
            flash('File[' + filename + '] uploaded.', 'success')
            blog_app.logger.info('file [%s] uploaded' % (filename or ''))
        else:
            flash('File invalid!', 'danger')
            blog_app.logger.warning('when uploading, file not valid')
        return redirect(url_for('user.manage', target='file'))
    return render_template('user/upload_file.html', form=form)


@login_required
@user.route('/download_file/<filename>')
def download_file(filename=None):
    log_request('download file[%s]' % (filename or ''))
    if filename is None:
        flash('file name empty', 'warning')
        blog_app.logger.warning('when downloading file, file name empty')
        return redirect(url_for('user.manage', target='file'))
    filename = secure_filename(filename)
    blog_app.logger.debug('when downloading file, file name is [%s]' % (filename or ''))
    upload_folder = blog_app.config['WINDBLOG_UPLOAD_FOLDER']
    upload_folder_path = os.path.join(os.getcwd(), upload_folder)
    filepath = os.path.join(upload_folder, filename);
    file = Path(filepath)
    if not file.is_file():
        flash('file not exists', 'warning')
        blog_app.logger.warning('when downloading, file [%s] not exists' % filename)
        return redirect(url_for('user.manage', target='file'))
    blog_app.logger.info('download file [%s] success' % (filename or ''))
    return send_from_directory(directory=upload_folder_path, filename=filename)


@login_required
@user.route('/delete_file/<filename>')
def delete_file(filename=None):
    log_request('delete file[%s]' % (filename or ''))
    if filename is None:
        flash('file name empty', 'warning')
        return redirect(url_for('user.manage', target='file'))
    filename = secure_filename(filename)
    upload_folder = blog_app.config['WINDBLOG_UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename);
    file = Path(filepath)
    if not file.is_file():
        flash('file not exists', 'warning')
        blog_app.logger.warning('when deleting file, file %s not exists' % filename)
        return redirect(url_for('user.manage', target='file'))
    file.unlink()
    flash('file ' + filename + ' deleted', 'success')
    return redirect(url_for('user.manage', target='file'))


@login_required
@user.route('/download_proxy', methods=['GET', 'POST'])
def download_proxy():
    log_request('proxy download')
    form = DownloadProxyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            blog_app.logger.debug('proxy download form data : [%s]' % form.to_json())
            url = form.url.data
            filename = url.split('/')[-1]
            if url is None:
                flash('url empty')
                return redirect(url_for('user.download_proxy'))
            req = get(url, stream=True)
            response = Response(stream_with_context(req.iter_content(chunk_size=1024*1024)), content_type=req.headers['content-type'])
            response.headers['Content-Disposition'] = 'attachment;filename=%s' % filename
            flash('proxy download success')
            return response
        else:
            flash('please check the url and try again', 'warning')
            blog_app.logger.warning('when proxying downloading, url not valid')
    return render_template('user/download_proxy.html', form=form)

