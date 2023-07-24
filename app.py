from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)
con = sqlite3.connect('data.db')
db = con.cursor()


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":

        _username = request.form.get("username")
        _password = request.form.get("password")
        _confirmation = request.form.get("confirmation")
        if(_password != _confirmation):
            return render_template("error.html")
        if(_password == "" or _confirmation == "" or _username == ""):
            return render_template("error.html")

        _usernamelist = db.execute("SELECT username FROM users WHERE username = ?", _username)

        if(_usernamelist):
            return render_template("error.html")
 
        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", _username, generate_password_hash(_password))
        db.commit()

        return redirect("/")

@app.route("/login")
def login():
    #session.clear()
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        _username = request.form.get("username")
        _password = request.form.get("password")
        return redirect("/")
    
    