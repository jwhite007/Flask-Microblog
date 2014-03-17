from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random


class User(db.Model):
    """docstring for User"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    pw_hash = db.Column(db.String())
    add_date = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean)
    confirm_date = db.Column(db.DateTime)
    reg_key = db.Column(db.String(20), unique=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, email, passwd):
        self.username = username
        self.email = email.lower()
        self.set_passwd(passwd)
        self.confirmed = False
        self.confirm_date = None
        add_date = datetime.utcnow()
        self.add_date = add_date
        self.create_regkey()

    def set_passwd(self, passwd):
        self.pw_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.pw_hash, passwd)

    def create_regkey(self):
        self.reg_key = ''.join(random.choice(string.ascii_uppercase +
                               string.ascii_lowercase + string.digits)
                               for i in range(20))

    def set_confirm_date(self):
        self.confirm_date = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username


tags = db.Table('tags',
                db.Column('tag_id', db.Integer,
                db.ForeignKey('tag.id')),
                db.Column('post_id', db.Integer,
                db.ForeignKey('post.id')))


class Post(db.Model):
    # __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title, body, tags, user_id):
        self.title = title
        self.body = body
        pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.user_id = user_id
        self.tags = tags

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    # __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name
