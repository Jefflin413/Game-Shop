import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game, Composer
from collections import defaultdict

bp = Blueprint('composer', __name__, url_prefix='/composer')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:composer_url>', methods=('GET', 'POST'))
def composer_page(composer_url):
    conn = my_db.get_conn()
    cname = unquote(composer_url)
    context = defaultdict(list)
    cursor = conn.execute("SELECT d.gname FROM dub d, composer c WHERE d.cname=c.cname AND c.cname='%s'" % cname)
    for result in cursor:
        gname = result[Game.GNAME.value]
        context['games'].append((gname, '/../game/' + quote(gname)))
        context[Composer.CNAME.value] = cname
    cursor = conn.execute("SELECT iname FROM canplay WHERE cname='%s'" % cname)
    for result in cursor:
        context[Composer.INAME.value].append(result[Composer.INAME.value])
    cursor = conn.execute("SELECT mgenre FROM Hasperformed WHERE cname='%s'" % cname)
    for result in cursor:
        context[Composer.MUSIC_GENRE.value].append(result[Composer.MUSIC_GENRE.value])
    cursor.close()
    return render_template("composer.html", **context)
