from flask_script import Command, Option


class GunicornApp(Command):

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = (
            Option(*klass.cli, dest=klass.name, default=klass.default)
            for setting, klass in settings.items() if klass.cli
        )
        return options

    def __call__(self, app=None, *args, **kwargs):

        from gunicorn.app.wsgiapp import WSGIApplication

        class FlaskApplication(WSGIApplication):

            def __init__(self, *args, **kwargs):
                super(FlaskApplication, self).__init__(*args, **kwargs)
            def init(self, parser, opts, args):
                return kwargs

            def load(self):
                return app

        FlaskApplication().run()
