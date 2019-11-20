from flask import Blueprint
from flask import render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("mod_main/view_home.html")

@main.route("/info/")
def view_info():
    return render_template('mod_main/view_info.html')