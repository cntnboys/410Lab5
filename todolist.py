import sqlite3
from flask import Flask, render_template, g


database = "test.db"

app = Flask(__name__)


@app.route("/")
def welcome():
    return "<h1> Welcome to CMPUT 410 - Jinja lab </h1>"


@app.route('/task', methods = ['GET', 'POST'])
def task():
    return render_template('show_entries.html', tasks = query_db('select * from tasks'))



@app.route("/login", methods = ["GET", "POST"])

def login():
    return render_template("login.html", error = None)


    
#function for giving you the connection
def get_conn():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        #return object connect
        #name and value
        db.row_factory = sqlite3.Row
    return db 
    
#Query the db
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    cur.close()
    return result


@app.teardown_appcontext
#close connection
def close_conn(exeption):
    db = getattr(g, '_database', None)
    if db != None:
        db.close()
        db = None\


if __name__ =='__main__':
    app.debug = True
    app.run()
