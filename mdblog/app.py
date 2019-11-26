from flask import Flask
from flask import render_template
from .models import db
from .models import User

from .mod_main import main
from .mod_blog import blog
from .mod_admin import admin

import os

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

if "MDBLOG_CONFIG" in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")
db.init_app(flask_app)

flask_app.register_blueprint(main)
flask_app.register_blueprint(blog)
flask_app.register_blueprint(admin, url_prefix="/admin")

@flask_app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500

@flask_app.errorhandler(404)
def internal_server_error(error):
    return render_template("errors/404.html"), 404

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