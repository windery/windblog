from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Email, Length, DataRequired, Regexp, EqualTo
from wtforms import ValidationError
from .models import User


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 100)])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 16)])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 100)])
    username = StringField('username', validators=[DataRequired(), Regexp('^[a-zA-z][a-zA-Z0-9_.]*$', 0, message='username must have only letters')])
    password = PasswordField('password', validators=[DataRequired(), Length(1, 16), EqualTo('confirm_password', message='password must match')])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')

