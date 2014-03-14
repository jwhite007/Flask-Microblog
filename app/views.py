from flask import render_template, flash, redirect
from app import app
# from forms import LoginForm


@app.route('/')
@app.route('/index')
def show_posts():
    # posts = read_posts()
    # return render_template('show_posts.html', posts=posts)
    post = {'title': 'this is a post title'}
    return render_template('show_posts.html', post=post)


@app.route('/add_post')
def add_post():
    return render_template('add_post.html')


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route("/login", methods=["GET", "POST"])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     # login and validate the user...
    #     login_user(user)
    #     flash("Logged in successfully.")
    #     # return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html")

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


@app.route('/logout')
def logout():
    # session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     form = LoginForm()
#     return render_template('login.html',
#         title = 'Sign In',
#         form = form)
