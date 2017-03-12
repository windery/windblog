from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Login')

