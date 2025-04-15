from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import DateField
from wtforms.fields.choices import SelectField
from wtforms.validators import ValidationError, InputRequired, Length, Email

class TaskBookingForm(FlaskForm):
    