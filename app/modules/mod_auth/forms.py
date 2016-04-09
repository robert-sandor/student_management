from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired


class LoginForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [DataRequired(message='Must provide a password :(')])