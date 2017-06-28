from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, PasswordField, FileField, StringField
from wtforms.validators import Length, DataRequired

import json

class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Login')


class FileForm(FlaskForm):
    file =  FileField(validators=[FileRequired()])
    submit = SubmitField('Save')

    def to_json(self):
        file_dict = []
        file_dict[self.file.label] = self.file.data.filename
        file_dict[self.submit.label] = self.submit.data
        return json.dumps(file_dict)

class DownloadProxyForm(FlaskForm):
    url = StringField('Download Url', validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField('Download')

    def to_json(self):
        proxy_dict = []
        proxy_dict[self.url.label] = self.url.data
        proxy_dict[self.submit.label] = self.submit.data
        return json.dumps(proxy_dict)
