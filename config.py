#!venv/bin/python3
# -*- coding:utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pandoo'
    SQLALCHEMY_DATABASE_URI = os.getenv('BLOG_DB_URI')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SUBJECTS = [
        ('technique', u'技术', '/technique'),
        ('environment', u'环境', '/environment'),
        ('resources', u'资源', '/resources'),
        ('thoughts', u'思考', '/thoughts')
    ]


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):

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
