from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """docstring for User"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    add_date = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, email, passwd,):
        # self.author = author
        self.username = username
        self.email = email
        self.passwd = passwd
        add_date = datetime.utcnow()
        self.add_date = add_date

    def set_password(self, passwd):
        self.pw_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.pw_hash, passwd)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        # self.auth or = author
        self.title = title
        self.body = body
        pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title