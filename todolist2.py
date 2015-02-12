import sqlite3
from flask import Flask, render_template, g, redirect, url_for, session, request, flash, abort


database = "test.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "cam"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
def welcome():
    return "<h1> Welcome to CMPUT 410 - Jinja lab </h1>"


@app.route('/task', methods = ['GET', 'POST'])
def task():
    if request.method == "POST":
        if not session.get('logged_in'):
            abort(401)
        Id = request.form['id']
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        addTask(Id,category,priority,description)
        flash("you have added succesfully")
        return redirect(url_for('task'))
    
    return render_template('show_entries.html', tasks = query_db('select * from tasks'))



@app.route("/login", methods = ["GET", "POST"])

def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
            
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"        
            
            
        else:
            session["logged_in"] = True
            flash("You are logged in")
            return redirect(url_for('task'))
            
    return render_template("login.html", error = error)


@app.route("/logout")
def logout():
    session.pop("logged_in")
    flash("You are logged out")
    return redirect(url_for('task'))

@app.route("/delete", methods = ["POST"])
def delete():
    if not session.get("logged_in"):
        abort(401)
    removetask(request.form['category'],request.form['priority'],request.form['description'])
    flash("task was deleted successfully")
    return redirect(url_for('task'))



def removetask(category,priority,description):
    query_db('delete from tasks where category = ? and priority = ? and description = ?' , [category, priority, description], one = True)
    get_db().commit()
    
def addTask(id, category,priority,description):
    query_db('insert into tasks values (?,?,?,?)', [id,category, priority ,description])
    get_db().commit()
    
    
#function for giving you the connection
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        #return object connect
        #name and value
        db.row_factory = sqlite3.Row
    return db 
    
#Query the db
def query_db(query, args=(), one=False):
    cur = get_db().cursor()
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
