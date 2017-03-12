# -*- coding:utf8 -*-

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
# from .permissions import Permissions
from app import login_manager
from random import seed
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from flask import current_app as app


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(128))
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     qq = db.Column(db.String(255), unique=True, nullable=True)
#     register_time = db.Column(db.DateTime, default=datetime.utcnow)
#     last_login_time = db.Column(db.DateTime, nullable=True)
#     about = db.Column(db.TEXT, nullable=True)
#     photo = db.Column(db.Binary, nullable=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
#
#     comment = db.relationship('Comment', backref='user')

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
    def insert_administrator():
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

#     @staticmethod
#     def generate_fake(count=100):
#         from forgery_py import lorem_ipsum, date, internet
#
#         seed()
#         for i in range(count):
#             u = User()
#             u.email = internet.email_address()
#             u.username = internet.user_name(True)
#             u.password = lorem_ipsum.word()
#             u.register_time = date.date()
#             u.about = lorem_ipsum.sentence()
#             if User.query.filter(or_(User.email==u.email, User.username==u.username)).first() is None:
#                 db.session.add(u)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()


# class Role(db.Model):
#     __tablename__ = 'role'
#     id = db.Column(db.Integer, primary_key=True)
#     role_name = db.Column(db.String(255), nullable=False, unique=True)
#     permission = db.Column(db.Integer, nullable=False)
#     user = db.relationship('User', backref='role')
#
#     @classmethod
#     def insert_roles(cls):
#         roles = {
#             'administrator': 0xff,
#             'user':
#                 Permissions.WRITE_ARTICLES
#                     | Permissions.COMMENT
#         }
#         for role_name in roles:
#             role = Role.query.filter_by(role_name=role_name).first()
#             if role is None:
#                 role = Role()
#             role.permission = roles[role_name]
#             db.session.add(role)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             db.session.rollback()
#
#     def __repr__(self):
#         return '<Role %r>' % self.role_name
#

