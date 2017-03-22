from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, PasswordField, FileField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Login')


class FileForm(FlaskForm):
    file =  FileField(validators=[FileRequired()])
    submit = SubmitField('Save')
