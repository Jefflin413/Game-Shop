import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game, Developer

bp = Blueprint('developer', __name__, url_prefix='/developer')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:developer_url>', methods=('GET', 'POST'))
def developer_page(developer_url):
    conn = my_db.get_conn()
    dname = unquote(developer_url)
    context = {'games':[]}
    cursor = conn.execute("SELECT * FROM produce p, developer d WHERE p.dname = d.dname AND d.dname='%s'" % dname)
    for result in cursor:
        context[Developer.DNAME.value] = result[Developer.DNAME.value]
        context[Developer.LOCATION.value] = result[Developer.LOCATION.value]
        context[Developer.STARTED.value] = result[Developer.STARTED.value]
        gname = result[Game.GNAME.value]
        context['games'].append((gname, '/../game/' + quote(gname)))
    cursor.close()
    return render_template("developer.html", **context)

