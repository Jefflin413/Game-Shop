import functools
from urllib.parse import quote, unquote
from sqlalchemy import text
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
from .global_values import Game, Producer, Developer, Composer
from flaskr.auth import login_required

bp = Blueprint('game', __name__, url_prefix='/game')
my_db = db

# connects to our database
@bp.before_request
def before_request():
    my_db.start()

# close our database
@bp.teardown_request
def teardown_request(exception):
    my_db.close(exception)

@bp.route('/<string:game_url>', methods=('GET', 'POST'))
def game_page(game_url):
    conn = my_db.get_conn()
    gname = unquote(game_url)
    context = {}
    cursor = conn.execute("SELECT * FROM game g WHERE g.gname='%s'" % gname)
    for result in cursor:
        context[Game.DESCRIPTION.value] = result[Game.DESCRIPTION.value]
        context[Game.GENRE.value] = result[Game.GENRE.value]
        context[Game.DATE.value] = result[Game.DATE.value]
        context[Game.PRICE.value] = result[Game.PRICE.value]
        context[Game.GNAME.value] = result[Game.GNAME.value]
        tmp = conn.execute("SELECT p.dname FROM game g, produce p WHERE p.gname=g.gname AND g.gname='%s'" % gname).fetchone()
        if tmp:
            context[Developer.DNAME.value] = tmp[Developer.DNAME.value]
            context['developer_url'] = "/../developer/" + quote(tmp[Developer.DNAME.value])
        tmp = conn.execute("SELECT n.pname FROM game g, notablework n WHERE n.gname=g.gname AND g.gname='%s'" % gname).fetchone()
        if tmp:
            context[Producer.PNAME.value] = tmp[Producer.PNAME.value]
            context['producer_url'] = "/../producer/" + quote(tmp[Producer.PNAME.value])
        tmp = conn.execute("SELECT d.cname FROM game g, dub d WHERE g.gname=d.gname AND g.gname='%s'" % gname).fetchone()
        if tmp:
            context[Composer.CNAME.value] = tmp[Composer.CNAME.value]
            context['composer_url'] = "/../composer/" + quote(tmp[Composer.CNAME.value])
        print(result)
    cursor.close()
    return render_template("game.html", **context)

@bp.route('/<string:gname>add_to_wishlist', methods=('POST',))
@login_required
def add_to_wishlist(gname):
    conn = my_db.get_conn()
    in_wish = conn.execute("SELECT * FROM Wish_List W WHERE W.account = '%s' AND W.gname = '%s'" % (g.user, gname)).fetchone()
    if not in_wish:
        cursor = conn.execute("INSERT INTO Wish_List (account, gname) VALUES ('%s', '%s')" % (g.user, gname))
        cursor.close()
    return redirect(url_for('wishlist.index'))

@bp.route('/<string:gname>remove_from_wishlist', methods=('POST',))
@login_required
def remove_from_wishlist(gname):
    conn = my_db.get_conn()
    in_wish = conn.execute("SELECT * FROM Wish_List W WHERE W.account = '%s' AND W.gname = '%s'" % (g.user, gname)).fetchone()
    if in_wish:
        print('i delete')
        cursor = conn.execute("DELETE FROM Wish_List WHERE account='%s' AND gname='%s'" % (g.user, gname))
        cursor.close()
    else:
        print('i do not delete')
    return redirect(url_for('wishlist.index'))
