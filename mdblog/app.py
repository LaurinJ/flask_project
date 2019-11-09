from flask import Flask, url_for
from flask import render_template
from .database import articles
from flask import request
from flask import redirect
from flask import session
from flask import g
from flask import flash

import os
import sqlite3

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

if "MDBLOG_CONFIG" in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")

@flask_app.route("/")
def index():
    return render_template("view_home.html")

@flask_app.route("/blogs/", methods=["GET"])
def view_blogs():
    db = get_db()
    cur = db.execute("select * from articles order by id desc ")
    articles = cur.fetchall()
    return render_template('view_blogs.html', articles=articles)

@flask_app.route("/blogs/", methods=["POST"])
def add_blogs():
    db = get_db()
    db.execute("insert into articles (title, content) values (?, ?)",
               [request.form.get("title"), request.form.get("content")])
    db.commit()
    flash("article was saved", "alert-successful")
    return redirect(url_for("view_blogs"))

@flask_app.route("/info/")
def view_info():
    return render_template('view_info.html')

@flask_app.route("/admin/")
def view_admin():
    if "logged" not in session:
        flash("you must be logged in", "alert-danger")
        return redirect(url_for("view_login"))
    return render_template('view_admin.html')

@flask_app.route("/blog/<int:art_id>")
def view_blog(art_id):
    db = get_db()
    cur = db.execute("select * from articles where id=(?)",[art_id])
    article = cur.fetchone()
    if article:
        return render_template("view_blog.html", article=article)
    return render_template('article_not_found.html', art_id=art_id)

@flask_app.route("/login/", methods=["GET"])
def view_login():
    return render_template("login.html")

@flask_app.route("/login/", methods=["POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == flask_app.config["USERNAME"] and password == flask_app.config["PASSWORD"]:
            session["logged"] = True
            flash("login successful", "alert-successful")
            return redirect(url_for("view_admin"))
        else:
            flash("login fail", "alert-fail")
            return redirect(url_for("view_login"))

@flask_app.route("/logout/", methods=["POST"])
def logout_user():
    session.pop("logged")
    return redirect(url_for("index"))

# UTILS
def connect_db():
    rv = sqlite3.connect(flask_app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite.db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        with open("mdblog/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()

# @flask_app.route("/blog/<string:name>/")
# def blog(name):
#     a = "Bouha {}".format(name)
#     return a
#
# # with flask_app.test_request_context():
# #     print(url_for('pozdrav', name="peter pan", cislo=5478))
#
# @flask_app.route("/hi/<string:name>/<int:cislo>/")
# def pozdrav(name, cislo):
#     a = url_for('pozdrav', name=name, cislo=cislo)
#     return render_template("view_home.html")