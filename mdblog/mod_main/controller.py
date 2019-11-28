from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from mdblog.mod_main.forms import NewsletterForm
from mdblog.models import Newsletter
from mdblog.models import db


main = Blueprint("main", __name__)

@main.route("/")
def view_welcame_page():
    return render_template("mod_main/view_home.html")

@main.route("/info/")
def view_info():
    return render_template('mod_main/view_info.html')

@main.route("/newsletter/", methods=["POST"])
def add_newsletter():
    newsletter_form = NewsletterForm(request.form)
    if newsletter_form.validate():
        newsletter = Newsletter(email=newsletter_form.email.data)
        db.session.add(newsletter)
        db.session.commit()
        flash("You were successfully subscribed", "alert-successful")
    else:
        for error in newsletter_form.errors:
            flash("{} is not valid".format(error), "alert-fail")
    return redirect(url_for("main.view_welcame_page"))