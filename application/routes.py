from flask import render_template, url_for, request, redirect
from application.forms.registration_form import ClientRegistrationForm, WorkerRegistrationForm
from application.data import clients, tradespeople
from application.data_access import add_client, add_tradesperson
from application import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',
                           head="home",
                           title="My Home Heroes",
                           subheading="need a hand? call our heroes!",
                           img1='static/images/squiggle2.png',
                           img2='static/images/squiggle.png',
                           img3='static/images/wideshot4.jpg')

@app.route('/welcome/client')
def welcome_client():
    return render_template('welcome_client.html', 
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Explore and browse our services', 
                            img3='static/images/paint.jpeg')

@app.route('/welcome/tradesperson')
def welcome_tradesperson():
    return render_template('welcome_tradesperson.html',
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Let''s get started!', 
                            img='static/images/wideshot.jpg')


@app.route('/register/client')
def register_client():
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
            return redirect(url_for('welcome_client'))
        
    return render_template('welcome_client.html', 
                           form=client_register, 
                           head='welcome', 
                           title='Account Successfully Created!', 
                           name=first_name, subheading='Explore & browse our services.', 
                           img='static/images/paint.jpeg')



@app.route('/register/tradesperson')
def register_tradesperson():
    error = ""
    worker_register = WorkerRegistrationForm()

    if request.method == 'POST':
        first_name = worker_register.first_name.data
        last_name = worker_register.last_name.data
        profession = worker_register.profession.data
        town = worker_register.town.data
        email = worker_register.email.data
        password = worker_register.password.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please supply both a first and last name'
        else:
            tradespeople.append({'Firstname': first_name, 'Lastname': last_name, 'Profession': profession, 'Town': town, 'Email': email, 'Password': password})
            add_tradesperson(first_name, last_name, email, password)
            return redirect(url_for('welcome_tradesperson'))
    
    return render_template('welcome_tradesperson.html', 
                           form=worker_register, 
                           head='welcome', 
                           title='Account Successfully Created!', 
                           name=first_name, subheading='Let''s get started!', 
                           img='static/images/wideshot.jpg')