#!venv/bin/python3
# -*- coding:utf8 -*-

import json

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired, Email
from config import Config



class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 100)])
    content = TextAreaField('content', validators=[DataRequired()])
    subject = SelectField('subject', validators=[DataRequired()], choices=[(s[0], s[0]) for s in Config.SUBJECTS])
    tags = StringField('tags')
    submit = SubmitField('publish')

    def to_json(self):
        post_dict = []
        post_dict[self.title.label] = self.title.data
        post_dict[self.content.label] = self.content.data
        post_dict[self.subject.label] = self.subject.data
        post_dict[self.tags.label] = self.tags.data
        return json.dumps(post_dict)


class CommentForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 255)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Comment')

    def to_json(self):
        comment_dict = []
        comment_dict[self.username.label] = self.username.data
        comment_dict[self.email.label] = self.email.data
        comment_dict[self.content.label] = self.content.data
        comment_dict[self.submit.label] = self.submit.data
        return json.dumps(comment_dict)

