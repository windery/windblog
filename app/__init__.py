#!venv/bin/python3
# -*- coding:utf8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .blog import blog_blueprint
    app.register_blueprint(blog_blueprint)
    from .user import user_blueprint
    app.register_blueprint(user_blueprint)

    @app.context_processor
    def subject_processor():
        from app.blog import models
        subjects = models.Subject.query.all()
        return dict(subjects=subjects)

    return app



