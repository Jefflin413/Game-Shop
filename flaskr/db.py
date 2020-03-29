from sqlalchemy import *
from flask import g

DATABASEURI = "mysql://username:password@server/db"
# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)


def start():
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None
    global connection
    connection = g.conn

def get_conn():
    # get the connection to the database
    return connection

def close(exception):
    try:
        g.conn.close()
    except Exception as e:
        pass
