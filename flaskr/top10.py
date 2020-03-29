import functools
from sqlalchemy import text
from urllib.parse import quote, unquote
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game

bp = Blueprint('top10', __name__)
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/top10', methods=('GET', 'POST'))
def top10():
    conn = my_db.get_conn()
    recommend = False
    cursor = conn.execute("""SELECT G.gname
                                            FROM Game G, Contain C
                                            WHERE G.gname=C.gname
                                            GROUP BY G.gname
                                            ORDER BY COUNT(*)::REAL DESC
                                            LIMIT 10;""")

    name_urls = []
    for idx, result in enumerate(cursor):
        name_urls.append((result[Game.GNAME.value], '/game/' + quote(result[Game.GNAME.value]), idx+1))

    cursor.close()
    context = {}
    context['name_urls'] = name_urls
    return render_template("top10.html", **context)

