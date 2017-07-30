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
        post_dict = {}
        post_dict[self.title.name] = self.title.data
        post_dict[self.content.name] = self.content.data
        post_dict[self.subject.name] = self.subject.data
        post_dict[self.tags.name] = self.tags.data
        return json.dumps(post_dict)

