from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://TechnoMonk@localhost/microblogdb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# class User(db.Model):
#     """docstring for User"""
#     id = db.Column(db.Integer, primary_key=True)
#     # author = db.Column(db.String(30))
#     username = db.Column(db.String(50), unique=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column()
#     add_date = db.Column(db.DateTime)

#     def __init__(self, username, email, passwd,):
#         # self.author = author
#         self.username = username
#         self.email = email
#         self.passwd = passwd
#         add_date = datetime.utcnow()
#         self.add_date = add_date

#     def set_password(self, passwd):
#         self.pw_hash = generate_password_hash(passwd)

#     def check_password(self, passwd):
#         return check_password_hash(self.pw_hash, passwd)

#     def __repr__(self):
#         return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # author = db.Column(db.String(30))
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User',
    #                        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, author):
        self.author = author
        self.title = title
        self.body = body
        pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


def write_post(title, body):
    name = Post(title, body)
    db.session.add(name)
    db.session.commit()


def read_posts():
    return Post.query.all()


def read_post(id):
    try:
        return Post.query.filter_by(id=id).one()
    except NoResultFound, e:
        return e



if __name__ == '__main__':
    manager.run()

# Notes for dropping tables:
#   db.session.remove()
#   db.drop_all()

# Notes for migrate:
#   python microblog.py db init
#   python microblog.py db migrate
#   python microblog.py db upgrade
#   python microblog.py db --help
