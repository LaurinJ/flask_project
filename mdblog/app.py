from flask import Flask, url_for
from flask import render_template

flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return render_template("welcome.html", text="ahoj jak je jinjo >D")

@flask_app.route("/hi/<string:name>/<int:cislo>/")
def pozdrav(name, cislo):
    a = url_for('pozdrav', name=name, cislo=cislo)
    return a

# with flask_app.test_request_context():
#     print(url_for('pozdrav', name="peter pan", cislo=5478))

@flask_app.route("/blog/<string:name>/")
def blog(name):
    a = "Bouha {}".format(name)
    return a