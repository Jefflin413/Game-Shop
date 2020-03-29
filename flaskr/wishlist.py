import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db
from .global_values import Wish_List 

import random 
import string
import datetime

bp = Blueprint('wishlist', __name__)
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)


@bp.route('/wishlist')
@login_required
def index():
    conn = my_db.get_conn()
    cursor = conn.execute("SELECT * FROM Wish_List W WHERE W.account='%s'" % g.user)
    name_urls = []
    for result in cursor:
        name_urls.append((result[Wish_List.GNAME.value], '/game/' + quote(result[Wish_List.GNAME.value])))
    cursor.close()
    context = {}
    context['name_urls'] = name_urls
    return render_template("wishlist.html", **context)

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    conn = my_db.get_conn()
    if request.method == 'POST':
        tid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        while conn.execute("SELECT * FROM Attend_Transaction T WHERE T.tid='%s'" % tid).fetchone():
            tid = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
        price = conn.execute("SELECT SUM(G.price) FROM Wish_List W, Game G WHERE W.account='%s' AND G.gname = W.gname" % g.user).fetchone()[0]
        timestamp = datetime.date.today()
        account = g.user
        payment = request.form['payment']
        print("give me all the variables: ", tid, price, timestamp, account, payment)
        conn.execute("INSERT INTO Attend_Transaction (tid, price, timestamp, account, payment) VALUES ('%s', '%s', '%s', '%s', '%s')" % (tid, price, timestamp, account, payment))
        cursor = conn.execute("SELECT G.gname FROM Wish_List W, Game G WHERE W.account='%s' AND G.gname=W.gname" % g.user)
        for i in cursor:
            conn.execute("INSERT INTO Contain (gname, tid) VALUES ('%s', '%s')" %(i[0], tid))
            conn.execute("DELETE FROM Wish_List WHERE account='%s' AND  gname='%s'" %(account, i[0]))
        cursor.close()
        return redirect(url_for('transaction_history.transaction_history'))
    return render_template('wishlist/checkout.html')

        
        

