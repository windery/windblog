#!venv/bin/python3
# -*- coding:utf8 -*-

from . import db
from config import Config
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), db.ForeignKey('subject.name'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(100))

    comment = db.relationship('Comment', backref=db.backref('post'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    content = db.Column(db.TEXT(500))
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
#            print('name : ' + s['name'] + ', route : ' + s['route'])
#            print('name : ' + subject.name + ', route : ' + subject.route)
            if subject is None:
                subject = Subject(name=s[0], name_ch=s[1], route=s[2])
                db.session.add(subject)
        db.session.commit()
