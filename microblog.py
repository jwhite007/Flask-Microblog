from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import Template
from flask import render_template
from flask import url_for
from flaskext.bcrypt import Bcrypt

# app = Flask(__name__)
# app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://TechnoMonk@localhost/microblogdb'
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
from app import app

bcrypt = Bcrypt(app)  # overwrites bcrypt module if needed in future.

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# login_manager = LoginManager()
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(userid):
#     return User.get(userid)


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


def hash_passwd(passwd):
    bcrypt.generate_password_hash(passwd)


def check_passwd(entry, hashed):
    bcrypt.check_password_hash(entry, hashed)


# @app.route('/')
# def show_posts():
#     posts = read_posts()
#     return render_template('show_posts.html', posts=posts)


# @app.route('/add_post')
# def add_post():
#     return render_template('add_post.html')


# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return 'Post %d' % post_id


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     # form = LoginForm()
#     # if form.validate_on_submit():
#     #     # login and validate the user...
#     #     login_user(user)
#     #     flash("Logged in successfully.")
#     #     # return redirect(request.args.get("next") or url_for("index"))
#     return render_template("login.html")

# @app.route("/settings")
# @login_required
# def settings():
#     pass

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(somewhere)

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/logout')
# def logout():
#     # session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))

if __name__ == '__main__':
    # manager.run()
    app.run()
