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
                           img1='decoration/squiggle2.png',
                           img2='decoration/squiggle.png',
                           background_image='static/images/wideshot44.jpeg')

@app.route('/example')
def empty():
    return render_template('example.html',
                            head='Example',
                            title='This is an example webpage',
                            subheading='This is a subtitle',
                            background_image="/static/images/wideshot4.jpg")

@app.route('/welcome/client')
def welcome_client():
    return render_template('welcome_client.html', 
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Explore and browse our services', 
                            background_image='/static/images/paint.jpeg')


@app.route('/welcome/tradesperson')
def welcome_tradesperson():
    return render_template('welcome_tradesperson.html',
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Let''s get started!', 
                            background_image='/static/images/wield.jpg')


@app.route('/register/client', methods=['GET', 'POST'])
def register_client():
    error = ""
    client_register = ClientRegistrationForm()

    if request.method == 'POST':
        first_name = client_register.first_name.data
        last_name = client_register.last_name.data
        email = client_register.email.data
        password = client_register.password.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please provide both a first and last name'
        else:
            clients.append({'Firstname': first_name, 'Lastname': last_name, 'Email': email, 'Password': password})
            add_client(first_name, last_name, email, password)
            return redirect(url_for('welcome_client'))
        
    return render_template('register_client.html', 
                            form=client_register, 
                            message=error,
                            head='client sign up', 
                            title='⚒ Connect with us ⚒', 
                            subheading='Get in touch with our skilled team',
                            img1='decoration/arrowyellow.png',
                            img2='decoration/arrownavy.png',
                            background_image = '/static/images/wideshot2.jpeg')



@app.route('/register/tradesperson', methods=['GET', 'POST'])
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
            error = 'Please provide both a first and last name'
        else:
            tradespeople.append({'Firstname': first_name, 'Lastname': last_name, 'Profession': profession, 'Town': town, 'Email': email, 'Password': password})
            add_tradesperson(first_name, last_name, profession, town, email, password)
            return redirect(url_for('welcome_tradesperson'))
    
    return render_template('register_tradesperson.html', 
                            form=worker_register, 
                            message=error,
                            head='tradesperson sign up', 
                            title='⚒ Get Bookings Now! ⚒', 
                            subheading='Sign up and join our team of heroes',
                            img1='decoration/arrowyellow.png',
                            img2='decoration/arrownavy.png',
                            background_image='/static/images/wideshotb.jpeg')

@app.route('/electrician')
def example():
        return render_template('electrician.html',
                               head='Electrician',
                               title='Your Local Electrical Home Heroes Are Here!',
                               subheading='Flickering light, a faulty socket, or need a complete electrical overhaul? Home Heroes are on call!',
                               img1='decoration/squiggle2.png',
                               img2='decoration/squiggle.png',
                               background_image="/static/images/electrician1.jpg")
