import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Transaction, Contain
from flaskr.auth import login_required

bp = Blueprint('transaction', __name__, url_prefix='/transaction_history')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:tid>', methods=('GET', 'POST'))
@login_required
def transaction(tid):
    conn = my_db.get_conn()
    #gname = unquote(game_url)
    tid = tid
    context = {}
    cursor = conn.execute("SELECT * FROM Attend_Transaction T WHERE T.tid='%s' AND T.account='%s'" % (tid, g.user))
    if cursor.rowcount == 0:
        cursor.close()
        return redirect("/")
    for result in cursor:
        context[Transaction.TID.value] = result[Transaction.TID.value]
        context[Transaction.PRICE.value] = result[Transaction.PRICE.value]
        context[Transaction.TIMESTAMP.value] = result[Transaction.TIMESTAMP.value]
        context[Transaction.ACCOUNT.value] = result[Transaction.ACCOUNT.value]
        context[Transaction.PAYMENT.value] = result[Transaction.PAYMENT.value]
        tmp = conn.execute("SELECT C.gname FROM Contain C WHERE C.tid='%s'" % tid)
        name_urls = []
        for t in tmp:
            name_urls.append((t[Contain.GNAME.value], '/game/' + quote(t[Contain.GNAME.value])))
        context['name_urls'] = name_urls
    cursor.close()
    return render_template("transaction.html", **context)
