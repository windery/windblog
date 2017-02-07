from . import user_blueprint as user
from flask import render_template


@user.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@user.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@user.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500
