from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, InputRequired, Email, Length, EqualTo, DataRequired


def password_validation(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if len(password) >= 100:
        raise ValidationError('Password is too long.')
    

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)], render_kw={"class": "form-control"})
    submit = SubmitField('Next', render_kw={"class": "btn btn-primary btn-lg btn-block"})


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[InputRequired(), password_validation], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('new_password', message='Passwords must match.')], render_kw={"class": "form-control"})
    submit = SubmitField('Reset Password', render_kw={"class": "btn btn-primary btn-success btn-lg btn-block"})