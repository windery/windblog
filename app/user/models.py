# -*- coding:utf8 -*-

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from sqlalchemy.exc import IntegrityError
from flask import current_app as app


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @staticmethod
    def insert_administrator_in_not_exists():
        administrator = User.query.filter_by(username='admin').first()
        if administrator is None:
            administrator = User()
            administrator.username = 'admin'
            admin_password = app.config['BLOG_ADMIN_PASSWORD']
            if admin_password is None:
                app.logger.error('when adding administrator, no valid password set, program will exit')
                exit(-1);
            administrator.password = admin_password
            db.session.add(administrator)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

