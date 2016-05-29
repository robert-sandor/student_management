from flask.ext.wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired


class PasswdChangeForm(Form):
    old_password = PasswordField('Old Password', [DataRequired(message="Must provide old password!")])
    new_password = PasswordField('New Password', [DataRequired(message="Must provide new password!")])
    repeat_password = PasswordField('Repeat Password', [DataRequired(message="Must provide new password again!")])
