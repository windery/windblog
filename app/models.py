from .import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __repr__(self):
        return '<User %s>' % self.username

