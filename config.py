#!venv/bin/python3
# -*- coding:utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pandoo'
    SQLALCHEMY_DATABASE_URI = os.getenv('WINDBLOG_DB_URI')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WINDBLOG_POSTS_PER_PAGE = os.getenv('WINDBLOG_POSTS_PER_PAGE') or 10
    BLOG_ADMIN_PASSWORD = os.getenv('WINDBLOG_ADMINISTRATOR_PASSWORD') or None

    SUBJECTS = [
        ('technique', '技术'),
        ('environment', '环境'),
        ('resources', '资源'),
        ('thoughts', '思考')
    ]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app()
        #concrete error process
        pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
