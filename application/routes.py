from flask import render_template, url_for, request, redirect
from application.forms.registration_form import ClientRegistrationForm
from application.data import clients
from application.data_access import add_client
from application import app

@app.route('/')
@app.route('/home')
def home():
    error = ""
    client_register = ClientRegistrationForm()

    if request.method == 'POST':
        first_name = client_register.first_name.data
        last_name = client_register.last_name.data
        email = client_register.email.data
        password = client_register.password.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please supply both a first and last name'
        else:
            clients.append({'Firstname': first_name, 'Lastname': last_name, 'Email': email, 'Password': password})
            add_client(first_name, last_name, email, password)
            return redirect(url_for('welcome'))

    return render_template('home.html',
                           form=client_register,
                           message=error,
                           head="home",
                           title="My Home Heroes",
                           subheading="Here to help with your daily needs",
                           img='static/images/wideshot2.jpg')

@app.route('/welcome')
def welcome():
    client_register = ClientRegistrationForm()
    first_name = client_register.first_name.data
    return render_template('welcome.html', form=client_register, head='welcome', title='Account Successfully Created!', name=first_name, subheading='Explore and browse our services', img='static/images/paint.jpeg')
