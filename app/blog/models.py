#!venv/bin/python3
# -*- coding:utf8 -*-

from app import db
from config import Config
from datetime import datetime
from flask import current_app
from sqlalchemy import desc, distinct
from sqlalchemy.exc import IntegrityError
from random import seed


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), db.ForeignKey('subject.name'))
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    content_md = db.Column(db.Text)
    brief_content = db.Column(db.String(100))
    brief_content_md = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(100))

    tag = db.relationship('Tag', backref='post')

    @classmethod
    def delete_post_by_title(cls, title):
        Tag.delete_post(title)
        post = cls.query.filter_by(title=title).first()
        db.session.delete(post)

    @classmethod
    def delete_post_by_id(cls, id):
        post = cls.query.filter_by(id=id).first()
        post_title = post.title
        db.session.delete(post)
        cls.delete_post(post_title=post_title)

    @classmethod
    def get_post_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_latest_posts_by_subject(cls, subject_name):
        if subject_name is None:
            return cls.get_latest_posts()
        return cls.query.filter_by(subject_name=subject_name).order_by(desc(Post.modify_time)).all()

    @classmethod
    def get_posts(cls):
        return cls.query.all()

    @classmethod
    def get_latest_posts(cls):
        return cls.query.order_by(desc(cls.create_time)).limit(100).all()

    @classmethod
    def get_pagination(cls, page):
        posts_per_page = current_app.config['WINDBLOG_POSTS_PER_PAGE']
        pagination = cls.query.order_by(cls.create_time.desc()).paginate(page, per_page=posts_per_page, error_out=False)
        return pagination

    @classmethod
    def get_pagination_by_subject(cls, subject, page):
        posts_per_page = current_app.config['WINDBLOG_POSTS_PER_PAGE']
        pagination = cls.query.filter_by(subject_name=subject).order_by(cls.create_time.desc()).paginate(page, per_page=posts_per_page, error_out=False)
        return pagination

    @classmethod
    def get_pagination_by_tag(cls, tag, page):
        posts_per_page = current_app.config['WINDBLOG_POSTS_PER_PAGE']
        post_titles = db.session.query(Tag.post_title).filter_by(tag=tag).subquery()
        pagination = cls.query.filter(cls.title.in_(post_titles)).order_by(cls.create_time.desc()).paginate(page, per_page=posts_per_page, error_out=False)
        return pagination

    def get_content(self):
        return self.content

    def get_markdown_content(self):
        return self.content_md

    def get_brief_content(self):
        return self.brief_content

    def get_brief_markdown_content(self):
        return self.brief_content_md


    def get_tag_list(self):
        return self.tags.split(',')

    @classmethod
    def clear(cls):
        cls.query.delete()
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def __repr__(self):
        return '<Post %r>' % self.title


class Subject(db.Model):
    __tablename__ = 'subject'
    name = db.Column(db.String(50), primary_key=True)
    name_ch = db.Column(db.String(50), unique=True)

    post = db.relationship('Post', backref=db.backref('subject'), lazy='dynamic')

    @staticmethod
    def insert_subjects_if_not_exists():
        subjects = Config.SUBJECTS
        for s in subjects:
            subject = Subject.query.filter_by(name=s[0]).first()
            if subject is None:
                subject = Subject(name=s[0], name_ch=s[1])
                db.session.add(subject)
        db.session.commit()

    @staticmethod
    def clear():
        Post.query.delete()
        Subject.query.delete()
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


class Tag(db.Model):
    tag = db.Column(db.String(50), primary_key=True)
    post_title = db.Column(db.String(255), db.ForeignKey('post.title'), primary_key=True, nullable=False)

    @classmethod
    def delete_tag(cls, name):
        cls.query.filter_by(name=name).delete()
        db.session.commit()

    @classmethod
    def delete_post(cls, post_title):
        cls.query.filter_by(post_title=post_title).delete()
        db.session.commit()

    @classmethod
    def add_tags(cls, post_title, tags):
        if tags and post_title:
            for tag in tags:
                record = cls(tag=tag, post_title=post_title)
                db.session.add(record)
            db.session.commit()

    @classmethod
    def update_tags(cls, post_title, tags):
        if isinstance(tags, str):
            tags = tags.split(',')
        cls.delete_post(post_title=post_title)
        cls.add_tags(post_title, tags)

    @classmethod
    def get_tags(cls):
        records = db.session.query(cls.tag).distinct(cls.tag).all()
        tags = [record.tag for record in records]
        return tags


