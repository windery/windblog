from . import db
from config import Config

class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
#    subject = db.Column(db.String, db.ForeignKey('blog_subject.name'))
    subject = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    create_time = db.Column(db.Integer)
    modify_time = db.Column(db.Integer)
    tags = db.Column(db.String)

#    comment = db.relationship('BlogComment', foreign_keys=[], backref=db.backref('blog_post'))


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'
    id = db.Column(db.Integer, primary_key=True)
#    post_id = db.Column(db.Integer, db.ForeighKey('blog_post.id'))
#    post_id = db.Column(db.Integer)
#    parent_id = db.Column(db.Integer, db.ForeignKey('blog_comment.id'))
    content = db.Column(db.String)
    email = db.Column(db.String)
    time = db.Column(db.Integer)

#    parent = db.relationship('BlogComment', backref=db.backref('blog_comment'))


class BlogSubject(db.Model):
    __tablename__ = 'blog_subject'
    name = db.Column(db.String, primary_key=True)
    route = db.Column(db.String, unique=True)

#    post = db.relationship('BlogPost', backref=db.backref('blog_subject'))

    @staticmethod
    def insert_subjects():
        subjects = Config.SUBJECTS
        for s in subjects:
            subject = BlogSubject.query.filter_by(name=s['name'])
            if subject is None:
                subject = BlogSubject(name=s['name'], route=s['route'])
                db.session.add(subject)
        db.session.commit()
