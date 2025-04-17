from flask import render_template, url_for, request, redirect, session, flash
from application.forms.registration_form import ClientRegistrationForm, WorkerRegistrationForm
from application.data import clients, tradespeople
from application.data_access import add_client, add_tradesperson, get_client_by_email, get_tp_by_email, book_job
from application import app
import bcrypt

# --------------- Home Page --------------- #
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



# --------------- Sign up Pages --------------- #
@app.route('/register/client', methods=['GET', 'POST'])
def register_client():
    client_register = ClientRegistrationForm()

    if request.method == 'POST' and client_register.validate():
        first_name = client_register.first_name.data
        last_name = client_register.last_name.data
        date_of_birth = client_register.dob.data
        town = client_register.town.data
        email = client_register.email.data
        password = client_register.password.data

        clients.append({'Firstname': first_name, 'Lastname': last_name, 'Date of Birth': date_of_birth, 'Town': town, 'Email': email, 'Password': password})
        add_client(first_name, last_name, date_of_birth, town, email, password)

        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'client'

        return redirect(url_for('welcome_client', name=first_name))
        
    return render_template('register_client.html', 
                            form=client_register, 
                            head='client sign up', 
                            title='Connect with us', 
                            subheading='Get in touch with our skilled team',
                            img1='decoration/arrowyellow.png',
                            img2='decoration/arrow.png',
                            img3='decoration/arrowupyellow.png',
                            img4='decoration/arrowupblack.png',
                            background_image = '/static/images/wideshot2.jpeg')



@app.route('/register/tradesperson', methods=['GET', 'POST'])
def register_tradesperson():
    worker_register = WorkerRegistrationForm()

    if request.method == 'POST' and worker_register.validate():
        first_name = worker_register.first_name.data
        last_name = worker_register.last_name.data
        date_of_birth = worker_register.dob.data
        profession = worker_register.profession.data
        town = worker_register.town.data
        email = worker_register.email.data
        password = worker_register.password.data

        tradespeople.append({'Firstname': first_name, 'Lastname': last_name, 'Date of Birth': date_of_birth, 'Profession': profession, 'Town': town, 'Email': email, 'Password': password})
        add_tradesperson(first_name, last_name, date_of_birth, profession, town, email, password)

        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'tradesperson'
        
        return redirect(url_for('welcome_tradesperson', name=first_name))
    
    return render_template('register_tradesperson.html', 
                            form=worker_register, 
                            head='tradesperson sign up', 
                            title='Get Bookings Now!', 
                            subheading='Sign up and join our team of heroes',
                            img1='decoration/arroworange.png',
                            img2='decoration/arrow.png',
                            img3='decoration/arrowuporange.png',
                            img4='decoration/arrowupblack.png',
                            background_image='/static/images/wideshot6.jpeg')



# --------------- Welcome Pages --------------- #
# Change this to make it /welcome/<name>
@app.route('/welcome/client', methods=['GET'])
def welcome_client():
    name = request.args.get('name', 'Guest')
    return render_template('welcome_client.html',
                           name=name,
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Explore and browse our services',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/wideshot5.jpeg')


# Change this to make it /welcome/<name>
@app.route('/welcome/tradesperson', methods=['GET'])
def welcome_tradesperson():
    return render_template('welcome_tradesperson.html',
                            head='welcome', 
                            title='Account Successfully Created!', 
                            subheading='Let''s get started!',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/wideshotb.jpeg')



# --------------- Login Routes --------------- #
@app.route('/login/client', methods=['GET','POST'])
def login_client():
    email = request.form['client_email']
    password = request.form['client_password']

    client = get_client_by_email(email)
    if client and bcrypt.checkpw(password.encode('UTF-8'), client['password'].encode('UTF-8')):
        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'client'
        return redirect(url_for('client_dashboard', name=client['firstname']))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('home'))



@app.route('/login/tradesperson', methods=['GET', 'POST'])
def login_tradesperson():
    email = request.form['tp_email']
    password = request.form['tp_password']

    tradesperson = get_tp_by_email(email)
    if tradesperson and bcrypt.checkpw(password.encode('UTF-8'), tradesperson['password'].encode('UTF-8')):
        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'tradesperson'
        return redirect(url_for('welcome_tradesperson', name=tradesperson['firstname']))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('home'))


# --------------- Logout Route --------------- #
@app.route('/logout', methods=['POST'])
def logout():
    # session.clear()
    session.pop('user', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))    



# --------------- Dashboards --------------- #
@app.route('/client/dashboard')
def client_dashboard():
    return render_template('client_dashboard.html',
                           head='client dashboard',
                           title='your dashboard',
                           subheading='explore our services',
                           background_image='/static/images/interior.png')


@app.route('/task/dashboard')
def task_dashboard():
    return render_template('tp_dashboard.html',
                           head='task dashboard',
                           title='your dashboard',
                           subheading='view your profile',
                           background_image='/static/images/wideshot3.jpeg')



# --------------- Booking Pages --------------- #

# Client
@app.route('/booking/services', methods=['GET', 'POST'])
def book_service():
    if 'user' not in session:
        return redirect(url_for('home.html'))
    
    if request.method == 'POST':
        clientID = session['user']
        workerID = request.form['worker_id']
        taskID = request.form['task_id']
        service_start = request.form['service_start']
        service_end = request.form['service_end']
        townID = request.form['town_id']
        task_desc = request.form['task_desc']

        book_job(clientID, workerID, taskID, service_start, service_end, townID, task_desc)
    return render_template('book_service.html',
                           head="Book a tradesperson",
                           title='Book a tradesperson!',
                           subheading='your home rescue, just a click away',
                           background_image='/static/images/house3.jpg')






@app.route('/services/electrician')
def electrician():
        return render_template('electrician.html',
                               head='Electrician',
                               title='Your Local Electrical Home Heroes Are Here!',
                               subheading='Flickering light, faulty socket, or need an electrical overhaul? Home Heroes are on call!',
                               icon='electrical_services',
                               background_image="/static/images/electrician1.jpg")

@app.route('/services/painting')
def painting():
    return render_template('painting.html', 
                           head='Painting Services',
                           title='Painting',
                           subheading='Home needs a splash of colour? Call our painters',
                           icon='imagesearch_roller',
                           background_image='/static/paints/paint.jpeg')

@app.route('/services/lawn_care')
def lawn_care():
    return render_template('lawn_care.html',
                           head='Lawn Care Services',
                           title='Yardwork & Lawn Care',
                           subheading='need your hedges trimmed? look no further...',
                           icon='psychiatry',
                           background_image='/static/images/lawn3.jpg')

@app.route('/services/moving')
def moving():
    return render_template('moving.html',
                           head='Moving Services',
                           title='Moving Services',
                           subheading='need help moving items or houses? look no further...',
                           icon='deployed_code',
                           background_image='/static/images/Moving_background.png')

@app.route('/services/home_repairs')
def home_repairs():
    return render_template('home_repairs.html',
                           head='Home Repairs',
                           title='Home Repair Services',
                           subheading='From Leaks to Locks, We Handle It All!',
                           # icon=
                           background_image='/static/images/repairstwo.jpg')


@app.route('/services/plumbing')
def plumbing():
    return render_template('plumbing.html',
                            head='Plumbing',
                            title='Plumbing services',
                            subheading='Because even the best pipes have bad days',
                            icon='plumbing',
                            background_image="/static/images/pipes background.jpg")



@app.route('/reviews')
def reviews():
    return render_template('reviews.html',
                           head='reviews',
                           title='customer experiences',
                           subheading='review our work',
                           icon='sentiment_very_satisfied',
                           background_image='/static/images/gardener.jpeg')