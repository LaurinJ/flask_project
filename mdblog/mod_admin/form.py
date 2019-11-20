from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wtforms import TextAreaField


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