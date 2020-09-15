from flask import Flask, render_template, request, redirect
import pymysql as p

app = Flask(__name__)
""" 
Everything should be written within this
"""


@app.route('/index')
def index():
    return render_template("form.html")


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == "POST":
        title = request.form['title']
        details = request.form['details']
        date = request.form['date']

        serverName = "localhost"
        userName = "root"
        password = ""
        dbName = "todo"

        try:
            db = p.connect(serverName, userName, password, dbName)
            cr = db.cursor()
            sql = "insert into task(title,detail,date) values ('{}','{}','{}')".format(
                title, details, date)
            cr.execute(sql)
            db.commit()
            db.close()

            return redirect("/dashboard")
        except Exception:
            db.rollback()
            return "Error in connection"


@app.route('/dashboard')
def dashboard():
    serverName = "localhost"
    userName = "root"
    password = ""
    dbName = "todo"

    try:
        db = p.connect(serverName, userName, password, dbName)
        cr = db.cursor()
        sql = "SELECT * from task"
        cr.execute(sql)
        data = cr.fetchall()
        return render_template("dashboard.html", row=data)
    except Exception:

        return "<h1>Connection Failed<h2>"


@app.route('/delete/<rid>')
def delete(rid):
    serverName = "localhost"
    userName = "root"
    password = ""
    dbName = "todo"

    try:
        db = p.connect(serverName, userName, password, dbName)
        cr = db.cursor()
        sql = "DELETE from task WHERE id = '{}'".format(rid)
        cr.execute(sql)
        db.commit()
        db.close()
        return redirect('/dashboard')
    except Exception:

        return "<h1>Connection Failed<h2>"


@app.route('/edit/<rid>')
def edit(rid):
    serverName = "localhost"
    userName = "root"
    password = ""
    dbName = "todo"

    try:
        db = p.connect(serverName, userName, password, dbName)
        cr = db.cursor()
        sql = "SELECT * from task WHERE id = {}".format(rid)
        cr.execute(sql)
        data = cr.fetchone()

        return render_template("/editForm.html", row=data)
    except Exception:

        return "<h1>Connection Failed<h2>"


app.run()
