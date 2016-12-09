import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pandoo'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SUBJECTS = (
        {'name': u'主页', 'route': '/home'},
        {'name': u'技术', 'route': '/technique'},
        {'name': u'环境', 'route': '/environment'},
        {'name': u'资源', 'route': '/resources'},
        {'name': u'思考', 'route': '/thoughts'},
        {'name': u'关于', 'route': '/about'}
    )

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

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
