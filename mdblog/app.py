from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wtforms import TextAreaField

from .models import db
from .models import Article
from .models import User

import os


flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

if "MDBLOG_CONFIG" in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")

db.init_app(flask_app)

# Forms

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old_password", validators=[InputRequired()])
    new_password = PasswordField("New_password", validators=[InputRequired()])

# Route

@flask_app.route("/")
def index():
    return render_template("view_home.html")

@flask_app.route("/blogs/", methods=["GET"])
def view_blogs():
    articles = Article.query.order_by(Article.id.desc())
    return render_template('view_blogs.html', articles=articles)

@flask_app.route("/blogs/", methods=["POST"])
def add_blogs():
    if "logged" not in session:
        return redirect(url_for("view_login"))

    add_blogs = ArticleForm(request.form)
    if add_blogs.validate():
        new_blog = Article(
            title = add_blogs.title.data,
            content = add_blogs.content.data)
        db.session.add(new_blog)
        db.session.commit()
        flash("article was saved", "alert-successful")
        return redirect(url_for("view_blogs"))
    else:
        for error in add_blogs.errors:
            flash("{} is missing".format(error), "alert-fail")
        return redirect(url_for("add_blogs"))

@flask_app.route("/blogs/new/", methods=["GET"])
def view_add_blogs():
    if "logged" not in session:
        return redirect(url_for("view_login"))

    form = ArticleForm()
    return render_template("blog_editor.html", form=form)

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
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("view_blog.html", article=article)
    return render_template('article_not_found.html', art_id=art_id)

@flask_app.route("/blog/<int:art_id>/edit/", methods=["GET"])
def view_blog_edit(art_id):
    if "logged" not in session:
        flash("you must be logged in", "alert-danger")
        return redirect(url_for("view_login"))
    article = Article.query.filter_by(id=art_id).first()
    if article:
        form = ArticleForm()
        form.title.data = article.title
        form.content.data= article.content
        return render_template("blog_editor.html", form=form, article=article)
    return render_template("article_not_found.html", art_id=art_id)

@flask_app.route("/blog/<int:art_id>/edit/", methods=["POST"])
def view_edit(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    article = Article.query.filter_by(id=art_id).first()
    if article:
        edit_form = ArticleForm(request.form)
        if edit_form.validate():
            article.title = edit_form.title.data
            article.content = edit_form.content.data
            db.session.add(article)
            db.session.commit()
            flash("article was saved", "alert-successful")
            return redirect(url_for("view_blog", art_id=art_id))
        else:
            for error in edit_form.errors:
                flash("{} is missing".format(error), "alert-fail")
            return redirect(url_for("view_blog_edit"))


@flask_app.route("/login/", methods=["GET"])
def view_login():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)

@flask_app.route("/login/", methods=["POST"])
def login_user():
    login_form = LoginForm(request.form)
    if login_form.validate():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("login successful", "alert-successful")
            return redirect(url_for("view_admin"))
        else:
            flash("login fail", "alert-fail")
            return render_template("login.html",form=login_form)
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "alert-fail")
        return redirect(url_for("view_login"))

@flask_app.route("/logout/", methods=["POST"])
def logout_user():
    session.pop("logged")
    return redirect(url_for("index"))

@flask_app.route("/changepassword/", methods=["GET"])
def view_change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = ChangePasswordForm()
    return render_template("change_password.html", form=form)

@flask_app.route("/changepassword/", methods=["POST"])
def change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = ChangePasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password changed successful", "alert-successful")
            return redirect(url_for("view_admin"))
        else:
            flash("Invalid credentials", "alert-fail")
            return render_template("change_password.html", form=form)
    else:
        for error in form.errors:
            flash("{} is missing".format(error), "alert-fail")
        return render_template("change_password.html", form=form)

# CLI COMMAND
def init_db(app):
    with app.app_context():
        db.create_all()
        print("Create new DB")

        default_user = User(username="admin")
        default_user.set_password("admin")

        db.session.add(default_user)
        db.session.commit()
        print("default user was created")

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