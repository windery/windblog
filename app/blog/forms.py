from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SelectField, \
     TextAreaField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, NumberRange, DataRequired
from config import Config



# class RegisterForm(Form):
#     email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
#     username = StringField('Username', validators=[
#         Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, \
#                                           'username must have only leters,'\
#                                           'dots numbers or underscores')])
#     password = PasswordField('Password', validators=[
#         Required(), EqualTo('password2', message='Password must match.')])
#     password2 = PasswordField('Conform Password', validators=[Required()])
#     sex = SelectField('Sex', choices=[('male', '男'), ('female', '女')])
#     age = IntegerField('Age', validators=[
#         NumberRange(1, 150, '手误了吧... 要不就得成精喽')], default=0)
#     about_me = TextAreaField('About me', validators=[
#         Length(-1, 600, '你这是写自传吧... 长话短说！')], \
#         default='懒滴很，撒都莫有...')
#     submit = SubmitField('注册')
#
#     def validate_email(self, field):
#         if User.query.filter_by(email=field.data).first():
#             raise ValidationError
#
#     def validate_username(self, field):
#         if User.query.filter_by(username=field.data).first():
#             raise ValidationError

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 100)])
    content = TextAreaField('内容', validators=[DataRequired()])
    subject = SelectField('主题', validators=[DataRequired()], choices=Config.SUBJECT_VALUES)
    tags = StringField('标签')
    submit = SubmitField('发布')


