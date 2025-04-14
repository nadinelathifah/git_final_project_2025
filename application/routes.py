from flask import render_template, url_for, request, redirect, session
from application.forms.registration_form import ClientRegistrationForm, WorkerRegistrationForm
from application.data import clients, tradespeople
from application.data_access import add_client, add_tradesperson, find_user
from application import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',
                           head="home",
                           title="My Home Heroes",
                           subheading="need a hand? call our heroes!",
                           img1='decoration/squiggleblue.png',
                           img2='decoration/squiggleblue2.png',
                           background_image='static/images/wideshot44.jpeg')

@app.route('/example')
def example():
    return render_template('example.html',
                            head='Example',
                            title='This is an example webpage',
                            subheading='This is a subtitle',
                            img1='decoration/squiggle2.png',
                            img2='decoration/squiggle.png',
                            background_image="/static/images/example.jpg")

@app.route('/welcome/client')
def welcome_client():
    name = request.args.get('name', 'Guest')
    return render_template('welcome_client.html',
                           name=name,
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Explore and browse our services',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/paint.jpeg')


@app.route('/welcome/tradesperson')
def welcome_tradesperson():
    return render_template('welcome_tradesperson.html',
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Let''s get started!',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/wield.jpg')


@app.route('/register/client', methods=['GET', 'POST'])
def register_client():
    error = ""
    client_register = ClientRegistrationForm()

    if request.method == 'POST':
        first_name = client_register.first_name.data
        last_name = client_register.last_name.data
        date_of_birth = client_register.dob.data
        email = client_register.email.data
        password = client_register.password.data

        if len(first_name) == 0 or len(last_name) == 0:
            error = 'Please provide both a first and last name'
        else:
            clients.append({'Firstname': first_name, 'Lastname': last_name, 'Date of Birth': date_of_birth, 'Email': email, 'Password': password})
            add_client(first_name, last_name, date_of_birth, email, password)

            session['loggedIn'] = True
            session['username'] = first_name

            return redirect(url_for('welcome_client', name=first_name))
        
    return render_template('register_client.html', 
                            form=client_register, 
                            message=error,
                            head='client sign up', 
                            title='Connect with us', 
                            subheading='Get in touch with our skilled team',
                            img1='decoration/arrowyellow.png',
                            img2='decoration/arrownavy.png',
                            img3='decoration/arrowupyellow.png',
                            img4='decoration/arrowupblack.png',
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
                            title='Get Bookings Now!', 
                            subheading='Sign up and join our team of heroes',
                            img1='decoration/arroworange.png',
                            img2='decoration/arrownavy.png',
                            img3='decoration/arrowuporange.png',
                            img4='decoration/arrowupblack.png',
                            background_image='/static/images/wideshot6.jpeg')


@app.route('/login/client', methods=['GET', 'POST'])
def login_client():
    error = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'client' 

        try:
            user = find_user(email, role)
            if user[4] == password:
                session['loggedIn'] = True
                session['username'] = email
                session['role'] = role
                session['first_name'] = user[1]

                return redirect(url_for('welcome_client'))
            else:
                error = "Invalid credentials. Please try again."
        except ValueError as err:
            print('User does not exist.')
            error = "User does not exist. Please sign up first."
    return render_template('login_client.html', 
                           error=error,
                           head='Welcome Client',
                           title='welcome back',
                           subheading='let''s get started')


@app.route('/login/tradesperson', methods=['GET', 'POST'])
def login_tradesperson():
    error = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'tradesperson'

        try:
            user = find_user(email, role)
            if user[4] == password: 
                session['loggedIn'] = True
                session['username'] = email
                session['role'] = role
                session['first_name'] = user[1]

                return redirect(url_for('welcome_tradesperson'))
            else:
                error = "Invalid credentials. Please try again."
        except ValueError as err:
            print('User does not exist.')
            error = "User does not exist. Please sign up first."
    return render_template('login_tradesperson.html', 
                           error=error,
                           head='Welcome Tradesperson',
                           title='welcome back',
                           subheading='let''s get started')


app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))        


@app.route('/services/painting')
def painting():
    return render_template('painting.html', 
                           head='Painting Services',
                           title='Painting',
                           subheading='Home needs a splash of colour? Call our painters',
                           icon='imagesearch_roller',
                           background_image='/static/paints/painting.jpg')

@app.route('/services/lawn_care')
def lawn_care():
    return render_template('lawn_care.html',
                           head='Lawn Care Services',
                           title='Yardwork & Lawn Care',
                           subheading='need your hedges trimmed? look no further...',
                           icon='psychiatry',
                           background_image='/static/images/lawn3.jpg')

@app.route('/services/plumbing')
def plumbing():
    return render_template('plumbing.html',
                            head='Plumbing',
                            title='Plumbing',
                            subheading='Because even the best pipes have bad days',
                            img1='decoration/squiggle2.png',
                            img2='decoration/squiggle.png',
                            icon='imagesearch_roller',
                            background_image="/static/images/pipes background.jpg")
