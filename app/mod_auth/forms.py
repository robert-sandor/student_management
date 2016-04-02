from flask.ext.wtf import Form  # , RecatchaField

from wtforms import StringField, PasswordField  # BooleanField

from wtforms.validators import Required, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email Address', [Email(),
            Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
        Required(message='Must provide a password. ;-)')])
