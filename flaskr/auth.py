# 2019/11/8
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_conn
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    conn = my_db.get_conn()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        country = request.form['country']
        age = int(request.form['age'])
        name = request.form['name']
        pw = request.form['password']

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not pw:
            error = 'Password is required.'
        elif age < 18:
            error = 'Needs to be older than 18 years old.'
        elif conn.execute("SELECT account FROM Player P WHERE P.account = '%s'" % username).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        elif conn.execute("SELECT email FROM Player P WHERE P.email = '%s'" % email).fetchone() is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            conn.execute("""
                         INSERT INTO Player (account, email,  name, age, country, password)
                         VALUES ('%s', '%s', '%s', '%i', '%s', '%s')
                         """ % (username, email, name, age, country, pw))
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['password']
        conn = my_db.get_conn()
        error = None
        user = conn.execute("SELECT * FROM Player P WHERE P.account = '%s'" % username).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif pw != conn.execute("SELECT password FROM Player WHERE account='%s'" % username).fetchone()[0]:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['account']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #g.user = conn.execute("SELECT account FROM Player P WHERE P.account = '%s'" % user_id).fetchone()
        g.user = user_id


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
