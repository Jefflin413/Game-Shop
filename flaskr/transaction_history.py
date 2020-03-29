import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)

from flaskr.auth import login_required
from . import db
from .global_values import Transaction

bp = Blueprint('transaction_history', __name__)
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)


@bp.route('/transaction_history')
@login_required
def transaction_history():
    conn = my_db.get_conn()
    cursor = conn.execute("SELECT tid, timestamp FROM Attend_Transaction T WHERE T.account='%s'" % g.user)
    name_urls = []
    for result in cursor:
        name_urls.append((result[Transaction.TID.value], '/transaction_history/' + quote(result[Transaction.TID.value]), result[Transaction.TIMESTAMP.value]))
    cursor.close()
    context = {}
    context['name_urls'] = name_urls
    return render_template("transaction_history.html", **context)
