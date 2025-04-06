from flask import render_template, url_for, request, redirect
from application.forms.registration_form import RegistrationForm
from application.data import clients
from application.data_access import add_client
from application import app

@app.route('/')
@app.route('/home')
def home():
    error = ""
    registration_form = RegistrationForm()

    if request.method == 'POST':
        first_name = registration_form.first_name.data
        last_name = registration_form.last_name.data
        email = registration_form.email.data
        password = registration_form.password.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please supply both a first and last name'

        else:
            clients.append({'Firstname': first_name, 'Lastname': last_name, 'Email': email, 'Password': password})
            add_client(first_name, last_name, email, password)
            return redirect(url_for('welcome'))

    return render_template('home.html',
                           form=registration_form,
                           message=error,
                           head="home",
                           title="Hive Heroes",
                           subheading="Here to help with your daily needs",
                           img='static/images/wideshot4.jpg')

@app.route('/welcome')
def welcome():
    registration_form = RegistrationForm()
    first_name = registration_form.first_name.data
    return render_template('welcome.html', form=registration_form, head='welcome', title='Account Successfully Created!', name=first_name, subheading='Explore and browse our services', img='static/images/paint.jpeg')