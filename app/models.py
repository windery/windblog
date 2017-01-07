#!venv/bin/python3
# -*- coding:utf8 -*-

from . import db
from config import Config
from datetime import datetime
from sqlalchemy import desc


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    qq = db.Column(db.String(255), unique=True, nullable=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), db.ForeignKey('subject.name'))
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(100))

    comment = db.relationship('Comment', backref=db.backref('post'))

    @staticmethod
    def get_latest_posts_by_subject(subject_name):
        return Post.query.filter_by(subject_name=subject_name).order_by(desc(Post.modify_time)).all()

    @staticmethod
    def get_posts():
        return Post.query.all()

    @staticmethod
    def get_latest_posts():
        return Post.query.order_by(desc(Post.create_time)).limit(100).all()

    def get_brief_content(self):
        return str(self.content)[0:100]

    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    content = db.Column(db.TEXT)
    email = db.Column(db.String(100))
    time = db.Column(db.Integer)

    parent = db.relationship('Comment', remote_side=parent_id)


class Subject(db.Model):
    __tablename__ = 'subject'
    name = db.Column(db.String(50), primary_key=True)
    name_ch = db.Column(db.String(50), unique=True)
    route = db.Column(db.String(255), unique=True)

    post = db.relationship('Post', backref=db.backref('subject'), lazy='dynamic')

    @staticmethod
    def insert_subjects():
        subjects = Config.SUBJECTS
        for s in subjects:
            subject = Subject.query.filter_by(name=s[0]).first()
            if subject is None:
                subject = Subject(name=s[0], name_ch=s[1], route=s[2])
                db.session.add(subject)
        db.session.commit()
