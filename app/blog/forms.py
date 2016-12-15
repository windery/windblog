#!venv/bin/python3
# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SelectField, \
     TextAreaField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, NumberRange, DataRequired
from config import Config


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 100)])
    content = TextAreaField('内容', validators=[DataRequired()])
    subject = SelectField('主题', validators=[DataRequired()], choices=[(s[0], s[1]) for s in Config.SUBJECTS])
    tags = StringField('标签')
    submit = SubmitField('发布')

