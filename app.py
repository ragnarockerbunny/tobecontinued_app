from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, text
from datetime import date
import requests
import json
#init
app = Flask(__name__)
TMDB_API_KEY = "dbfe5734c22317eacd8ba6138bde414c"
#Session Config
app.config["SESSION_PERMANENT"] = False
app.config['SECRET_KEY'] = 'RGBW5189_42'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
#SQLAlchemy engine
engine = create_engine("sqlite+pysqlite:///data.db", echo=True)

#Helpers
def error(_message):
    return render_template("error.html", error = _message)

#Routes
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        _username = request.form.get("username")
        _password = request.form.get("password")

        if(_password == "" or _username == ""):
            return error("Fields cannot be left empty")

        with engine.connect() as db:
            _res = db.execute(text("SELECT id, username, hash FROM users WHERE username = :u"), {"u": _username}).all()
            print(_res)
            if not _res:
                return error("Username not found")

            if _res[0][1] != _username:
                return error("Something went wrong")

            if not check_password_hash(_res[0][2], _password):
                return error("Password is incorrect")

            #succesful login
            session["username"] = _username
            session["user_id"] = _res[0][0]
            return redirect("/")
        
        return error("Something went wrong")

@app.route("/logout")
def logout():
    session.clear();
    return render_template("logout.html")

@app.route("/")
def home():
    if "username" in session:
        _watchlist = []
        with engine.connect() as db:
            _unparsed = db.execute(text("SELECT * FROM watchlist WHERE user_id = :id ORDER BY date_added DESC"), {"id": session["user_id"]}).all()

        for row in _unparsed:
            _id = row[1]
            #_url = 'https://api.themoviedb.org/3/search/movie?query=' + _id + '&api_key=' + TMDB_API_KEY
            _url = 'https://api.themoviedb.org/3/movie/' + str(_id) + '?api_key=' + TMDB_API_KEY
            _response = requests.get(_url).json()

            #Example Response
            #{'adult': False, 'backdrop_path': '/7dzngS8pLkGJpyeskCFcjPO9qLF.jpg', 'belongs_to_collection': {'id': 404609, 'name': 'John Wick Collection', 'poster_path': '/xUidyvYFsbbuExifLkslpcd8SMc.jpg', 'backdrop_path': '/fSwYa5q2xRkBoOOjueLpkLf3N1m.jpg'}, 'budget': 20000000, 'genres': [{'id': 28, 'name': 'Action'}, {'id': 53, 'name': 'Thriller'}], 'homepage': 'https://www.lionsgate.com/movies/john-wick', 'id': 245891, 'imdb_id': 'tt2911666', 'original_language': 'en', 'original_title': 'John Wick', 'overview': 'Ex-hitman John Wick comes out of retirement to track down the gangsters that took everything from him.', 'popularity': 62.748, 'poster_path': '/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg', 'production_companies': [{'id': 23008, 'logo_path': '/5SarYupipdiejsEqUkwu1SpYfru.png', 'name': '87Eleven', 'origin_country': 'US'}, {'id': 36259, 'logo_path': None, 'name': 'DefyNite Films', 'origin_country': 'US'}, {'id': 36433, 'logo_path': None, 'name': 'MJW Films', 'origin_country': 'US'}, {'id': 3528, 'logo_path': '/cCzCClIzIh81Fa79hpW5nXoUsHK.png', 'name': 'Thunder Road', 'origin_country': 'US'}], 'production_countries': [{'iso_3166_1': 'US', 'name': 'United States of America'}], 'release_date': '2014-10-22', 'revenue': 88761661, 'runtime': 101, 'spoken_languages': [{'english_name': 'Hungarian', 'iso_639_1': 'hu', 'name': 'Magyar'}, {'english_name': 'English', 'iso_639_1': 'en', 'name': 'English'}, {'english_name': 'Russian', 'iso_639_1': 'ru', 'name': 'Pусский'}], 'status': 'Released', 'tagline': "Don't set him off.", 'title': 'John Wick', 'video': False, 'vote_average': 7.419, 'vote_count': 17806}

            _watchlist.append({"name" : _response["original_title"], "release_date" : _response["release_date"], "film_id": _id})

        return render_template("home.html", username = session["username"], watchlist = _watchlist)
    else:
        return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        _username = request.form.get("username")
        _password = request.form.get("password")
        _confirmation = request.form.get("confirmation")
        if(_password != _confirmation):
            return error("Passwords do not match")
        if(_password == "" or _confirmation == "" or _username == ""):
            return error("Fields cannot be left empty")
        
        with engine.connect() as db:
            _usernamelist = db.execute(text("SELECT username FROM users WHERE username = :u"), {"u": _username}).all()

        if(_usernamelist):
            return error("Username already exists")
 
        with engine.begin() as db:
            db.execute(text("INSERT INTO users(username, hash) VALUES (:u, :h)"), {"u":_username, "h":generate_password_hash(_password)})

        return redirect("/")

@app.route("/search", methods = ["GET", "POST"])
def search():
    if "username" in session:
        if request.method == "GET":
            return render_template("search.html")
        if request.method == "POST":
            _query = request.form.get("query")
            _url = 'https://api.themoviedb.org/3/search/movie?query=' + _query + '&api_key=' + TMDB_API_KEY
            _response = requests.get(_url)
            _results = _response.json()["results"]
            #print(json.dumps(_response.json(), sort_keys=True, indent=2))
            return render_template("searchresults.html", results = _results)
    else: 
        return redirect("/")

@app.route("/addToList", methods = ["POST"])
def addToList():
    #get id from post
    #append id to database
    #remember to commit as you go
    _item_id = request.form.get("item_id")
    if not _item_id:
        return error("Something went wrong with the film id")
    with engine.connect() as db:
        _userid = db.execute(text("SELECT id FROM users WHERE username = :u"), {"u": session["username"]}).all()
    if not _userid:
        return error("User ID not found")

    _userid = _userid[0][0]

    with engine.connect() as db:
        if db.execute(text("SELECT * FROM watchlist WHERE user_id = :uid AND film_id = :fid"), {"uid": session["user_id"], "fid": _item_id}).all():
            return error("Film already in watchlist")
        else:
            db.execute(text("INSERT INTO watchlist(user_id, film_id, date_added) VALUES (:uid, :fid, :d)"), {"uid": _userid, "fid":_item_id, "d": date.today().isoformat()})
            db.commit()
    
    return redirect("/")

@app.route("/remove", methods = ["POST"])
def remove():
    _film_id = request.form.get("film_id")
    with engine.connect() as db:
        db.execute(text("DELETE FROM watchlist WHERE user_id = :uid AND film_id = :fid"), {"uid": session["user_id"], "fid": _film_id})
        db.commit()

    return redirect("/")