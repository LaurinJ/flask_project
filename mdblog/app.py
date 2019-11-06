from flask import Flask, url_for
from flask import render_template
from .database import articles

flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return render_template("view_home.html")

@flask_app.route("/blogs/")
def view_blogs():
    return render_template('view_blogs.html', articles=articles.items())

@flask_app.route("/info/")
def view_info():
    return render_template('view_info.html')

@flask_app.route("/admin/")
def view_admin():
    return render_template('view_admin.html')

@flask_app.route("/blog/<int:art_id>")
def view_blog(art_id):
    article = articles.get(art_id)
    if article:
        return render_template("view_blog.html", article=article)
    return render_template('article_not_found.html', art_id=art_id)

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