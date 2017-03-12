#!venv/bin/python3
# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired
from config import Config


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 100)])
    content = TextAreaField('content', validators=[DataRequired()])
    subject = SelectField('subject', validators=[DataRequired()], choices=[(s[0], s[0]) for s in Config.SUBJECTS])
    tags = StringField('tags')
    submit = SubmitField('publish')

