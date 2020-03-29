import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game, Producer

bp = Blueprint('producer', __name__, url_prefix='/producer')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:producer_url>', methods=('GET', 'POST'))
def producer_page(producer_url):
    conn = my_db.get_conn()
    pname = unquote(producer_url)
    print(pname)
    context = {'games':[]}
    cursor = conn.execute("SELECT * FROM NotableWork n, producer p WHERE p.pname = n.pname AND p.pname='%s'" % pname)

    for result in cursor:
        context[Producer.PNAME.value] = result[Producer.PNAME.value]
        gname = result[Game.GNAME.value]
        context['games'].append((gname, '/../game/' + quote(gname)))
    cursor.close()
    print(context)
    return render_template("producer.html", **context)

