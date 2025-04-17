from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields import DateField
from wtforms.fields.choices import SelectField
from wtforms.validators import ValidationError, InputRequired, Length, Email

    
def password_validation(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one number.')
    if len(password) >= 100:
        raise ValidationError('Password is too long.')
    

class ClientRegistrationForm(FlaskForm):
    first_name = StringField('Firstname', validators=[InputRequired('Please fill in your first name.'), Length(max=100)], render_kw={'class':'form-control'})
    last_name = StringField('Lastname', validators=[InputRequired('Please fill in your surname.'), Length(max=150)], render_kw={'class':'form-control'})
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired('Please fill in your date of birth.')], render_kw={'class': 'form-control', 'type': 'date'})
    town = SelectField('Town', choices=[('', 'Choose your location'),
                                        ('1', 'Livingston'),
                                        ('2', 'Bathgate'),
                                        ('3', 'Broxburn'),
                                        ('4', 'Linlithgow'),
                                        ('5', 'Armadale'),
                                        ('6', 'Whitburn'),
                                        ('7', 'East Calder'),
                                        ('8', 'West Calder'),
                                        ('9', 'Blackburn'),
                                        ('10', 'Polbeth'),
                                        ('11', 'Kirknewton'),
                                        ('12', 'Uphall'),
                                        ('13', 'Winchburgh'),
                                        ('14', 'Dechmont'),
                                        ('15', 'Seafield')], render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[InputRequired('Please fill in your email address.'), Email('Please enter a valid email address.'), Length(max=150)], render_kw={'class':'form-control'})
    password = PasswordField('Password', validators=[InputRequired('Please fill in a password for your account.'), password_validation], render_kw={'class':'form-control'})
    submit = SubmitField('SIGN UP', render_kw={"class": "btn btn-primary btn-lg btn-block"})


class WorkerRegistrationForm(FlaskForm):
    first_name = StringField('Firstname', validators=[InputRequired('Please fill in your first name.'), Length(max=100)], render_kw={'class':'form-control'})
    last_name = StringField('Lastname', validators=[InputRequired('Please fill in your surname.'), Length(max=150)], render_kw={'class':'form-control'})
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired('Please fill in your date of birth.')], render_kw={'class': 'form-control', 'type': 'date'})
    profession = SelectField('Task', choices=[('', 'Choose your specialisation: '),
                                                    ('1', 'Painting'),
                                                    ('2', 'Home Repair'),
                                                    ('3', 'Moving'),
                                                    ('4', 'Electrician'),
                                                    ('5', 'Plumbing'),
                                                    ('6', 'Lawn Care')
                                                    ], render_kw={'class':'form-control'})
    town = SelectField('Town', choices=[('', 'Choose your location'),
                                        ('1','Livingston'),
                                        ('2', 'Bathgate'),
                                        ('3', 'Broxburn'),
                                        ('4', 'Linlithgow'),
                                        ('5', 'Armadale'),
                                        ('6', 'Whitburn'),
                                        ('7', 'East Calder'),
                                        ('8', 'West Calder'),
                                        ('9', 'Blackburn'),
                                        ('10', 'Polbeth'),
                                        ('11', 'Kirknewton'),
                                        ('12', 'Uphall'),
                                        ('13', 'Winchburgh'),
                                        ('14', 'Dechmont'),
                                        ('15', 'Seafield')], render_kw={'class':'form-control'})
    email = StringField('Email', validators=[InputRequired('Please fill in your email address.'), Email('Please enter a valid email address.'), Length(max=150)], render_kw={'class':'form-control'})
    password = PasswordField('Password', validators=[InputRequired('Please fill in a password for your account.'), password_validation], render_kw={'class':'form-control'})
    submit = SubmitField('SIGN UP', render_kw={"class": "btn btn-primary btn-lg btn-block"})