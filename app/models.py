from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db
from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.String(20))
    age = db.Column(db.Integer)
    about_me = db.Column(db.Text())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def password(self):
        raise AttibuteError('password is not a readable attibute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %s>' % self.username

@login_manager.user_loader
def user_loader(email):
    return User.query.get(email)
