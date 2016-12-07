from . import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.BigInteger(unsigned=True), primary_key=True, autoincrement=True)
    subject = db.Column(db.String, db.ForeignKey('subject.name'))
    title = db.Column(db.String)
    content = db.Column(db.Text(convert_unicode=False))
    create_time = db.DateTime(db.DateTime())
    modify_time = db.DateTime(db.DateTime())
    tags = db.Column(db.String)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.BigInteger(unsigned=True), primary_key=True, autoincrement=True)
    post_id = db.Column(db.BigInteger(unsigned=True), db.ForeighKey('post.id'))
    parent_id = db.Column(db.BigInteger(unsigned=True), db.ForeignKey('comment.id'))
    content = db.Column(db.String)
    email = db.Column(db.String)
    time = db.Column(db.DateTime)

class Subject(db.Model):
    __tablename__ = 'subject'
    name = db.Column(db.String, primary_key=True)
