from flask.ext.wtf import Form
from wtforms import (TextField, PasswordField,
                     TextAreaField, SubmitField, validators)
from wtforms.validators import Required
# from app import db
from models import User
from seasurf_form import SeaSurfForm


class RegistrationForm(SeaSurfForm):
    username = TextField('User Name',
                         [validators.Required()])
    # username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address',
                      [validators.Length(min=6, max=35),
                       validators.Email("This is not a valid email address")])
    passwd = PasswordField('New Password',
                           [validators.Required(),
                            validators.EqualTo('confirm',
                                               message="Passwords don't match")])
    confirm = PasswordField('Repeat Password', [validators.Required()])
    submit = SubmitField("Register")

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class LoginForm(SeaSurfForm):
    email = TextField('Email',
                      validators=[Required('Please enter your email address'),
                      validators.Email('Please enter your email address.')])
    passwd = PasswordField('Password',
                           validators=[Required('Please enter your password')])
    submit = SubmitField('Log On')
    # remember_me = BooleanField('remember_me', default=False)

    # def __inti__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_passwd(self.passwd.data):
            return True
        else:
            self.email.errors.append(
                'The email address you provided is not in the system. Please register.')
            return False


class AddPost(SeaSurfForm):
    post_title = TextField('Title', validators=[Required()])
    post_categories = TextField('categories', validators=[Required()])
    post = TextAreaField('Post', validators=[Required()])

    def validate(self):
        if not Form.validate(self):
            return False

        else:
            return True


