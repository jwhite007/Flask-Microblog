from flask.ext.wtf import Form
from wtforms import HiddenField
from flask import g
from app import app


class SeaSurfForm(Form):
    @staticmethod
    @app.before_request
    def add_csrf():
        csrf_name = app.config.get('CSRF_COOKIE_NAME', '_csrf_token')
        setattr(SeaSurfForm, csrf_name,
                HiddenField(default=getattr(g, csrf_name)))
