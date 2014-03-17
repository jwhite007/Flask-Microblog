from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Message, Mail
from flask.ext.seasurf import SeaSurf
# from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'qO6DIelqpEGFgKJjYNZbG6XnoPgTZP'

db = SQLAlchemy(app)
mail = Mail(app)
csrf = SeaSurf(app)

# login_manager = LoginManager()

from app import views, models, forms
