from flask import render_template, url_for, request, redirect, session, flash
from application.forms.registration_form import ClientRegistrationForm, WorkerRegistrationForm
from application.data import clients, tradespeople
from application.data_access import add_client, add_tradesperson, get_client_by_email, get_tp_by_email, book_job, get_all_tasks, get_all_towns, find_matching_tradespeople, get_reviews, get_client_by_id, get_tp_by_id, set_tp_profile, display_tp_profile, update_tradesperson_profile, update_tp_personal_info, display_client_profile, update_client_info, get_towns_with_ids, get_tasks_with_ids, get_client_bookings
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

# This route directs you to the client sign up page.
@app.route('/register/client', methods=['GET', 'POST'])
def register_client():

    # Here we're creating an instance object (client_register) from the ClientRegistrationForm() class, which is a subclass we made from FLaskForm WTForms (check registration_form.py)
    # GET method enables us to display the form.
    client_register = ClientRegistrationForm()

    # This condition states that if the form was submitted via 'POST' method, and the values submitted into the form (within the input field) are valid (i.e. passed all the validators shown in registration_form.py),
    # then, proceed to retrieve the data that the user submitted to the form:
    if request.method == 'POST' and client_register.validate():
        first_name = client_register.first_name.data
        last_name = client_register.last_name.data
        date_of_birth = client_register.dob.data
        town = client_register.town.data
        email = client_register.email.data
        password = client_register.password.data

        check_existing_email = get_client_by_email(email)
        if check_existing_email:
            flash("Email already exists. Please use a different email address to sign up, or if an account exists, please login.", "error")
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

        try:
            # Append the extracted data into a list so that you can render the list onto the page and show data.
            clients.append({'Firstname': first_name, 'Lastname': last_name, 'Date of Birth': date_of_birth, 'Town': town, 'Email': email, 'Password': password})
            # Use the add_client() function (check data_access.py) to insert that data into the clients table in the SQL database.
            client_id = add_client(first_name, last_name, date_of_birth, town, email, password)
        except ValueError as valueError:
            flash(str(valueError), "error") 
        except Exception:
            flash("Something went wrong during registration. Please try again.", "error")
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

        # Session variables (in Flask), are temporary data stored on the server-side to identify who the user is, keep track of user requests and login status. 
        # They act like a dictionary, session['key'] = value, that stores info specific to a user during their visit (i.e. their "session").
        # Session variables recognise the user as being logged in when they sign up.
        session['loggedIn'] = True
        # The user is identified by their unique email address.
        session['user'] = email
        # Makes it known that the user that just registered is a client.
        session['role'] = 'client'
        session['client_id'] = client_id

        # Here once the form is submitted, and user clicks 'Sign up', it redirects them to a welcome page where their first name is passed through.
        return redirect(url_for('welcome_client'))
        
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
    # GET method enables us to display the tradesperson sign up form.
    worker_register = WorkerRegistrationForm()

    if request.method == 'POST' and worker_register.validate():
        first_name = worker_register.first_name.data
        last_name = worker_register.last_name.data
        date_of_birth = worker_register.dob.data
        profession = worker_register.profession.data
        town = worker_register.town.data
        email = worker_register.email.data
        password = worker_register.password.data

        check_existing_email = get_tp_by_email(email)
        if check_existing_email:
            flash("Email already exists. Please use a different email address to sign up, or if an account exists, please login.", "error")
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

        try:
            tradespeople.append({'Firstname': first_name, 'Lastname': last_name, 'Date of Birth': date_of_birth, 'Profession': profession, 'Town': town, 'Email': email, 'Password': password})
            worker_id = add_tradesperson(first_name, last_name, date_of_birth, profession, town, email, password)
        except ValueError as valueError:
            flash(str(valueError), "error") 
        except Exception:
            flash("Something went wrong during registration. Please try again.", "error")
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

        session['loggedIn'] = True
        session['user'] = email
        # Makes it known that the user that just registered is a tradesperson.
        session['role'] = 'tradesperson'
        session['worker_id'] = worker_id
        return redirect(url_for('welcome_tradesperson'))
    
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

# Client Reg Confirmation and Welcome Message
@app.route('/welcome/client', methods=['GET'])
def welcome_client():
    # Get the clientID from the session and use get_client_by_id() (check data_access.py) to retrieve their ID from the database clients table.
    # Purpose: retrieve the client's name to show welcome message but also ensure that only people who have logged in can access this page.
    client_id = session.get('client_id')
    # Get 'loggedIn' from the session. But if 'loggedIn' doesn't exist, default to 'False'.
    logged_in = session.get('loggedIn', False)

    # If it's not the correct client and this person is not logged in, redirect them to the login page.
    if not client_id and not logged_in:
        return redirect(url_for('login_client')) 
    
    client = get_client_by_id(client_id)

    # If it is the correct client, retrieve their firstname from the clients table in DB.
    if client:
        name = client['firstname']
        welcome_message = f"Welcome, {name}!" 

        return render_template('welcome_client.html',
                            name=name,
                            head=welcome_message,
                            title=welcome_message,
                            subheading='Account Successfully Created! Please explore your dashboard',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/houses.jpg')
    
    return redirect(url_for('login_client'))


# Tradesperson Reg Confirmation and Welcome Message
@app.route('/welcome/tradesperson', methods=['GET'])
def welcome_tradesperson():
    worker_id = session.get('worker_id')
    logged_in = session.get('loggedIn', False)

    if not worker_id and not logged_in:
        return redirect(url_for('login_tradesperson'))
    
    tradesperson = get_tp_by_id(worker_id)
    
    if tradesperson:
        name = tradesperson['firstname']
        welcome_message = f"Welcome, {name}!"
        return render_template('welcome_tradesperson.html',
                            name=name,
                            head=welcome_message,
                            title=welcome_message,
                            subheading='Let''s get started. Please explore your dashboard',
                            img1='decoration/squiggleblue.png',
                            img2='decoration/squiggleblue2.png',
                            background_image='/static/images/wideshotb.jpeg')
    
    return redirect(url_for('login_tradesperson'))




# --------------- Login Routes --------------- #

# Client
# This route defines the client login endpoint which handles GET and POST HTTP requests.
# This route is triggered when the user navigates to the login page for clients. 
@app.route('/login/client', methods=['GET','POST'])
def login_client():
    # Get the values that the user entered into the login form.
    # This retrieves the email that the user has inputted in the form field with name="client_email" (check layout.html on the client-login section)
    email = request.form.get('client_email')
    # This retrieves the password inputted in form field with name="client_password"
    password = request.form.get('client_password')

    # get_client_by_email() function (check data_access.py) queries the DB to check if there's a record of a client with the given email.
    # If a client with that email exists in the DB, it returns the client's details; if not, returns none (you can check this by running the data_access.py file & looking at the terminal).
    client = get_client_by_email(email)

    # Next step checks whether the password they've entered matches the one that's in the DB for that email.
    # if client - checks if the client was returned by get_client_by_email() query.
    # bcrypt.checkpw() - checks if the password entered by the user matches the hashed password stored in the DB. If it does, returns True.
    # client['password'].encode('UTF-8') retrieves hashed password stored in DB & converts it into bytes.
    if client and bcrypt.checkpw(password.encode('UTF-8'), client['password'].encode('UTF-8')):
        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'client'
        session['client_id'] = client['clientID']
        return redirect(url_for('client_dashboard'))
    else:
        flash("Invalid email or password", "error")
        return redirect(url_for('home'))
    


# Tradesperson login route
@app.route('/login/tradesperson', methods=['GET', 'POST'])
def login_tradesperson():
    email = request.form.get('tp_email')
    password = request.form.get('tp_password')

    tradesperson = get_tp_by_email(email)
    if tradesperson and bcrypt.checkpw(password.encode('UTF-8'), tradesperson['password'].encode('UTF-8')):
        session['loggedIn'] = True
        session['user'] = email
        session['role'] = 'tradesperson'
        session['worker_id'] = tradesperson['workerID']
        return redirect(url_for('task_dashboard'))
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
    client_id = session.get('client_id')
    client = get_client_by_id(client_id)

    firstname = client['firstname'] if client else 'Client'
    greeting = f"Welcome Back, {firstname}!"

    head = f"{firstname}'s Dashboard"

    bookings = get_client_bookings(client_id)

    return render_template('client_dashboard.html',
                           name=firstname,
                           bookings=bookings,
                           head=head,
                           title=greeting,
                           subheading='Explore your dashboard',
                           background_image='/static/images/interior.png')


@app.route('/task/dashboard')
def task_dashboard():
    worker_id = session.get('worker_id')
    tradesperson = get_tp_by_id(worker_id)

    firstname = tradesperson['firstname'] if tradesperson else 'Tasker'
    greeting = f"Welcome Back, {firstname}!"

    head = f"{firstname}'s Dashboard"

    return render_template('tp_dashboard.html',
                           head=head,
                           name=firstname,
                           title=greeting,
                           subheading='View your dashboard', 
                           background_image='/static/images/wideshot3.jpeg')



# --------------- Client Booking Pages --------------- #

# Client - Search for a tradesperson to choose.
@app.route('/find_tradesperson', methods=['GET', 'POST'])
def find_tradesperson():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    towns = get_all_towns()
    tasks = get_all_tasks()
    results = []

    if request.method == 'POST':
        location = request.form['location']
        task = request.form['task']
        hourly_rate = request.form['hourly_rate']
        star_rating = request.form['star_rating']

        results = find_matching_tradespeople(task, location, hourly_rate, star_rating)

    return render_template('find_tradesperson.html', 
                           towns=towns, 
                           tasks=tasks, 
                           results=results,
                           head="find a tradesperson",
                           title="find & book your home hero!",
                           subheading="get your task done now",
                           background_image='/static/images/mansion.png')


# Client - after choosing the tradesperson, book them.
@app.route('/book_service', methods=['GET', 'POST'])
def book_service():
    if request.method == 'POST':
        # Retrieve the data from the form
        clientID = session.get('client_id')  # Get the logged-in client's ID from the session
        workerID = request.form.get('worker_id')
        taskID = request.form.get('task_id')
        service_start = request.form['service_start']
        service_end = request.form['service_end']
        task_description = request.form['task_description']

        # Call the function to book the job and insert into the database
        book_job(clientID, workerID, taskID, service_start, service_end, task_description)

        if not workerID.isdigit() or not taskID.isdigit():
            return "Error: Invalid workerID or taskID", 400

        # Redirect to a confirmation page or back to the tradesperson's page
        return redirect('/client_dashboard')

    # Handle the GET request: this is where the user will be directed after clicking "Book This Tradesperson"
    # Handle GET request to display the form and passed values
    worker_id = request.args.get('workerID')
    task_id = request.args.get('taskID')

    # For debugging
    print(f"workerID: {worker_id}, taskID: {task_id}") 

    # Retrieve the tradesperson's workerID and full name via get_tp_by_id() function.
    tradesperson = get_tp_by_id(worker_id)
    name = tradesperson['firstname'] + " " + tradesperson['lastname']

    return render_template('book_service.html',
                           tradesperson=tradesperson, 
                           task_id=task_id,
                           worker_id=worker_id,
                           name = name,
                           head="Book a tradesperson",
                           title='Book a tradesperson!',
                           subheading='Your home rescue, just a click away',
                           background_image='/static/images/mansion.png')


@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html',
                           head="booking confirmed",
                           title="You have successfully booked!",
                           subheading="Please wait for confirmation from the tradesperson.",
                           background_image='/static/images/houses.jpeg')



# --------------- Tradesperson Booking Pages --------------- #

@app.route('/see_bookings')
def see_bookings():
    pass




# --------------- Client Profile --------------- #

@app.route('/client_profile', methods=['GET'])
def client_profile():

    client_id = session.get('client_id')
    client = get_client_by_id(client_id)
    firstname = client['firstname'] if client else 'Client'

    head = f"{firstname}'s profile"

    profile = display_client_profile(client_id)

    return render_template('client_profile.html',
                           head=head,
                           name = firstname,
                           profile=profile,
                           title="Your profile",
                           subheading="View or update your personal details",
                           background_image='/static/images/interior.png')


@app.route('/client_profile/update', methods=['GET', 'POST'])
def update_client_profile():
    towns = get_towns_with_ids()
    client_id = session.get('client_id')
    profile = display_client_profile(client_id)

    if request.method == 'POST':
        client_id = session.get('client_id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        townID = request.form.get('townID')

        update_client_info(client_id, firstname, lastname, townID)
        return redirect('/client_profile#client-profile')
    return render_template('client_profile_update.html',
                           towns=towns,
                           profile=profile,
                           head='update profile',
                           title="Your profile",
                           subheading="View or update your personal details",
                           background_image='/static/images/interior.png')



# --------------- Tradesperson Profile --------------- #

@app.route('/tradesperson_profile', methods=['GET'])
def tradesperson_profile():
    workerID = session.get('worker_id')
    profile = display_tp_profile(workerID)
    return render_template('tp_profile.html',
                           head='profile information',
                           profile=profile,
                           title='your profile',
                           subheading='choose from the following options below',
                           background_image='/static/images/wideshot3.jpeg')


@app.route('/tradesperson_profile/setup', methods=['GET', 'POST'])
def setup_tp_profile():
    workerID = session.get('worker_id')
    profile = display_tp_profile(workerID)

    if request.method == 'POST':
        workerID = session.get('worker_id')
        phone_number = request.form.get('phone_number')
        hourly_rate = request.form.get('hourly_rate')
        business = request.form.get('business')
        bio = request.form.get('bio')

        set_tp_profile(workerID, phone_number, hourly_rate, business, bio)
        profile = display_tp_profile(workerID)
    print("profile: ", profile)

    return render_template('tp_profile_setup.html',
                           profile = profile,
                           head='profile setup',
                           title='profile setup',
                           subheading='enable clients to see your details',
                           background_image='/static/images/wideshot3.jpeg')


@app.route('/tradesperson_profile/update/profile', methods=['GET', 'POST'])
def update_tp_profile():
    workerID = session.get('worker_id')
    profile = display_tp_profile(workerID)

    if request.method == 'POST':
        workerID = session.get('worker_id')
        phone_number = request.form.get('phone_number')
        hourly_rate = request.form.get('hourly_rate')
        business = request.form.get('business')
        bio = request.form.get('bio')

        update_tradesperson_profile(workerID, phone_number, hourly_rate, business, bio)
        profile = display_tp_profile(workerID)
    print("profile: ", profile)

    return render_template('tp_profile_update.html',
                           profile = profile,
                           head='profile setup',
                           title='profile setup',
                           subheading='enable clients to see your details',
                           background_image='/static/images/wideshot3.jpeg')


@app.route('/tradesperson_profile/update/personal', methods=['GET', 'POST'])
def update_tp_info():
    workerID = session.get('worker_id')
    profile = display_tp_profile(workerID)
    tasks = get_tasks_with_ids()
    towns = get_towns_with_ids()

    if request.method == 'POST':
        workerID = session.get('worker_id')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        taskID = request.form.get('taskID')
        townID = request.form.get('townID')

        update_tp_personal_info(workerID, firstname, lastname, taskID, townID)
        profile = display_tp_profile(workerID)
    print("profile: ", profile)

    return render_template('tp_update_personal_info.html',
                           profile = profile,
                           tasks=tasks,
                           towns=towns,
                           head='profile setup',
                           title='profile setup',
                           subheading='enable clients to see your details',
                           background_image='/static/images/wideshot3.jpeg')




# --------------- Services --------------- #
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
                           background_image='/static/images/gardening2.jpg')

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
                           background_image='/static/images/repairstwo.jpg')


@app.route('/services/plumbing')
def plumbing():
    return render_template('plumbing.html',
                            head='Plumbing',
                            title='Plumbing services',
                            subheading='Because even the best pipes have bad days',
                            icon='plumbing',
                            background_image="/static/images/plumbing_background.png")



@app.route('/reviews')
def reviews():
    show_review = get_reviews()
    print(show_review)
    return render_template('reviews.html',
                           head='reviews',
                           reviews = show_review,
                           title='customer experiences',
                           subheading='review our work',
                           icon='star',
                           background_image='/static/images/gardening.jpg')