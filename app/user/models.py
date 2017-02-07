# -*- coding:utf8 -*-

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from .permissions import Permissions
from app import login_manager


class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follow_time = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    qq = db.Column(db.String(255), unique=True, nullable=True)
    register_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_time = db.Column(db.DateTime, nullable=True)
    about = db.Column(db.TEXT, nullable=True)
    photo = db.Column(db.Binary, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    comment = db.relationship('Comment', backref='user')
    follwer = db.relationship('Follow',
                              foreign_keys=[Follow.followed_id],
                              backref=db.backref('follower', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

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

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False, unique=True)
    permission = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='role')

    @classmethod
    def insert_roles(cls):
        roles = {
            'administrator': 0xff,
            'user':
                Permissions.WRITE_ARTICLES
                    | Permissions.COMMENT
                    | Permissions.FOLLOW,
            'professional_user':
                Permissions.WRITE_ARTICLES
                    | Permissions.COMMENT
                    | Permissions.FOLLOW
                    | Permissions.FILE_SAVE
                    | Permissions.PROXY_DOWNLOAD
        }
        for role_name in roles:
            role = Role.query.filter_by(role_name=role_name).first()
            if role is None:
                role = Role()
            role.permission = roles[role_name]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.role_name



