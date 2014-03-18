from flask import Flask, render_template, flash, redirect, url_for, session, request, g, abort
# from wtforms import Form
from app import app
# from forms import Register, SubmitPost, RegistrationForm
from models import User, Post, Tag, tags
from app import db
from forms import LoginForm, AddPost, RegistrationForm
from app import mail
from app import Message
import string
import random


@app.route('/')
@app.route('/index', endpoint='homepage')
def show_posts():
    posts = get_posts()
    return render_template('show_posts.html', posts=posts)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate() is False:
            flash("All fields are required for registration.")
            return render_template('register.html', form=form)
        else:
            newuser = User(form.username.data,
                           form.email.data, form.passwd.data)
            db.session.add(newuser)
            db.session.commit()

            # obtuser = User.query.filter_by(email=form.email.data.lower()).first()
            email = newuser.email.encode('ascii', 'ignore')
            reg_key = newuser.reg_key.encode('ascii', 'ignore')
            subject = "Your confirmation email from microBLOG"
            mail_to_be_sent = Message(subject=subject, recipients=[newuser.email])
            conf_url = url_for('confirm', reg_key=reg_key, _external=True)
            mail_to_be_sent.body = "Please click the link to confirm registration at microBLOG: %s" % conf_url
            mail.send(mail_to_be_sent)
            flash('Please check your email to confirm registration.  Then you can start using the site.')
            # session['email'] = newuser.email
            return redirect(url_for('homepage'))

    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/confirm/<reg_key>', methods=['GET', 'POST'])
def confirm(reg_key):
    user = User.query.filter_by(reg_key=reg_key).first()
    if user is not None:
        user.confirmed = True
        user.set_confirm_date()
        db.session.commit()
        session['email'] = user.email
        # # flash(user.confirmed)
        flash('You have been confirmed %s.  You can start posting to the microBLOG' % user.username)
        return redirect(url_for('homepage'))
    else:
        # consider an error response in case someone is trying to crack.
        flash('Sorry.  That registration key does not exist')
        return redirect(url_for('homepage'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() is False:
            # flash('Your email address is not registered at microBLOG.  Please register')
            return render_template('login.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('homepage'))
    elif request.method == 'GET':
        return render_template('login.html',
                               title='Log On',
                               form=form)


def get_posts():
    return Post.query.all()


def get_users():
    return User.query.all()


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'email' not in session and request.method == 'GET':
        flash('You must login and/or register before creating a post.')
        return redirect(url_for('homepage'))
    else:
        form = AddPost()
        # if form.validate_on_submit():
        #     return redirect('/success')
        if request.method == 'POST':
            if form.validate() is False:
                return render_template('add_post.html', form=form)
            else:
                # db.session.add(Tag('testing'))
                # db.session.commit()
                user = User.query.filter_by(email=session['email']).first()
                tag_list = form.post_tags.data.split(',')
                tag_list2 = []
                for tag in tag_list:
                    tag_list2.append(tag.lstrip(' '))
                tag_list_final = []
                for tag in tag_list2:
                    if not Tag.query.filter_by(name=tag).first():
                        new_tag = Tag(tag)
                        db.session.add(new_tag)
                        db.session.commit()
                        tag_list_final.append(new_tag)
                    else:
                        old_tag = Tag.query.filter_by(name=tag).first()
                        tag_list_final.append(old_tag)
                newpost = Post(form.post_title.data, form.post.data,
                               tag_list_final, user.id)
                db.session.add(newpost)
                db.session.commit()
                return redirect(url_for('homepage'))
        else:
            return render_template('add_post.html', form=form)


@app.route('/pending')
def pending():
    return render_template('pending.html')


@app.route('/logout')
def logout():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        session.pop('email', None)
    flash('You were logged out')
    return redirect(url_for('homepage'))



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)










