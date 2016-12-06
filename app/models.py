from . import db

class Passage(db.Model):
    __tablename__ = 'passage'
    id = db.Column(db.BigInteger(unsigned=True), primary_key=True)
    text = db.Column(db.Text(convert_unicode=False))
    create_time = db.DateTime(db.DateTime())
    modify_time = db.DateTime(db.DateTime())