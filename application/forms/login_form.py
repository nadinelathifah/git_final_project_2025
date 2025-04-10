from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import InputRequired, EqualTo

class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')