#!venv/bin/python3
# -*- coding:utf8 -*-

import os
import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from logging.handlers import RotatingFileHandler

from config import config

# flask_bootstrap
bootstrap = Bootstrap()


# flask_sqlalchemy
db = SQLAlchemy()

# flask_login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'


def create_app(config_name):
    # create app
    app = Flask(__name__)

    # init configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # logging
    if not os.path.isdir('log'):
        os.mkdir('log')
    file_handler = RotatingFileHandler('log/windblog.log', maxBytes=1024*1024*10, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    str_format = '[%(asctime)s] p%(process)s [%(name)s:%(lineno)d] %(levelname)s - %(message)s'
    time_format = '%m-%d %H:%M:%S'
    formatter = logging.Formatter(str_format, time_format)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # init plugins
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    markdown = Markdown(app)

    # register blueprints
    from .blog import blog_blueprint
    app.register_blueprint(blog_blueprint)
    from .user import user_blueprint
    app.register_blueprint(user_blueprint)

    # add subjects to context for every page navbar
    @app.context_processor
    def subject_processor():
        from app.blog import models
        subjects = models.Subject.query.all()
        return dict(subjects=subjects)

    app.logger.info('windblog app created.')

    app.extensions['bootstrap']['cdns']['bootstrap'].fallback.baseurl='//cdn.bootcss.com/bootstrap/3.3.7/'

    return app



