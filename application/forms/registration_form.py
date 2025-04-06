from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import ValidationError, InputRequired

    
def password_validation(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if len(password) >= 100:
        raise ValidationError('Password is too long.')
    

class RegistrationForm(FlaskForm):
    first_name = StringField('Firstname', validators=[InputRequired('Please fill in your first name.')], render_kw={'class':'form-control'})
    last_name = StringField('Lastname', validators=[InputRequired('Please fill in your surname.')], render_kw={'class':'form-control'})
    email = StringField('Email', validators=[InputRequired('Please fill in your email address.')], render_kw={'class':'form-control'})
    password = PasswordField('Password', validators=[InputRequired('Please fill in a password for your account.'), password_validation], render_kw={'class':'form-control'})
    submit = SubmitField('SIGN UP', render_kw={"class": "btn btn-primary btn-lg btn-block"})