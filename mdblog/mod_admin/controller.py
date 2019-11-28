from flask import Blueprint
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import g
from flask import flash

from .form import ArticleForm
from .form import ChangePasswordForm
from .form import LoginForm

from mdblog.models import db
from mdblog.models import Article
from mdblog.models import User

admin = Blueprint("admin", __name__)


@admin.route("/blogs/", methods=["POST"])
def add_blogs():
    if "logged" not in session:
        return redirect(url_for("admin.view_login"))

    add_blogs = ArticleForm(request.form)
    if add_blogs.validate():
        new_blog = Article(
            title = add_blogs.title.data,
            content = add_blogs.content.data,
            html_render = add_blogs.html_render.data)
        db.session.add(new_blog)
        db.session.commit()
        flash("article was saved", "alert-successful")
        return redirect(url_for("blog.view_blogs"))
    else:
        for error in add_blogs.errors:
            flash("{} is missing".format(error), "alert-fail")
        return redirect(url_for("admin.add_blogs"))

@admin.route("/blogs/new/", methods=["GET"])
def view_add_blogs():
    if "logged" not in session:
        return redirect(url_for("admin.view_login"))

    form = ArticleForm()
    return render_template("mod_admin/blog_editor.html", form=form)

@admin.route("/admin/")
def view_admin():
    if "logged" not in session:
        flash("you must be logged in", "alert-danger")
        return redirect(url_for("admin.view_login"))
    return render_template('mod_admin/view_admin.html')

@admin.route("/blog/<int:art_id>/edit/", methods=["GET"])
def view_blog_edit(art_id):
    if "logged" not in session:
        flash("you must be logged in", "alert-danger")
        return redirect(url_for("admin.view_login"))
    article = Article.query.filter_by(id=art_id).first()
    if article:
        form = ArticleForm()
        form.title.data = article.title
        form.content.data= article.content
        return render_template("mod_admin/blog_editor.html", form=form, article=article)
    return render_template("mod_blog/article_not_found.html", art_id=art_id)

@admin.route("/blog/<int:art_id>/edit/", methods=["POST"])
def view_edit(art_id):
    if "logged" not in session:
        return redirect(url_for("admin.view_login"))
    article = Article.query.filter_by(id=art_id).first()
    if article:
        edit_form = ArticleForm(request.form)
        if edit_form.validate():
            article.title = edit_form.title.data
            article.content = edit_form.content.data
            article.html_render = edit_form.html_render.data
            db.session.add(article)
            db.session.commit()
            flash("article was saved", "alert-successful")
            return redirect(url_for("blog.view_blog", art_id=art_id))
        else:
            for error in edit_form.errors:
                flash("{} is missing".format(error), "alert-fail")
            return redirect(url_for("admin.view_blog_edit"))


@admin.route("/login/", methods=["GET"])
def view_login():
    login_form = LoginForm()
    return render_template("mod_admin/login.html", form=login_form)

@admin.route("/login/", methods=["POST"])
def login_user():
    login_form = LoginForm(request.form)
    if login_form.validate():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            session["logged"] = user.username
            flash("login successful", "alert-successful")
            return redirect(url_for("admin.view_admin"))
        else:
            flash("login fail", "alert-fail")
            return render_template("mod_admin/login.html",form=login_form)
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "alert-fail")
        return redirect(url_for("mod_admin/view_login"))

@admin.route("/logout/", methods=["POST"])
def logout_user():
    session.pop("logged")
    return redirect(url_for("main.index"))

@admin.route("/changepassword/", methods=["GET"])
def view_change_password():
    if "logged" not in session:
        return redirect(url_for("admin.view_login"))
    form = ChangePasswordForm()
    return render_template("mod_admin/change_password.html", form=form)

@admin.route("/changepassword/", methods=["POST"])
def change_password():
    if "logged" not in session:
        return redirect(url_for("admin.view_login"))
    form = ChangePasswordForm(request.form)
    if form.validate():
        user = User.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password changed successful", "alert-successful")
            return redirect(url_for("admin.view_admin"))
        else:
            flash("Invalid credentials", "alert-fail")
            return render_template("mod_admin/change_password.html", form=form)
    else:
        for error in form.errors:
            flash("{} is missing".format(error), "alert-fail")
        return render_template("mod_admin/change_password.html", form=form)