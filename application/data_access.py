import mysql.connector
import bcrypt
import sys

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="homeheroes"
    )
    return mydb


def add_client(firstname, lastname, date_of_birth, town, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM clients where email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already exists")
        
        cursor.execute("SELECT COUNT(*) FROM tradespeople where email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already exists on the tradesperson side. Please login using the tradesperson route or Sign up with a different email.")
        
        encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))
        insert = "INSERT INTO clients (firstname, lastname, date_of_birth, townID, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (firstname, lastname, date_of_birth, town, email, encoded_password)
        cursor.execute(insert, values)
        connection.commit()
        print(f"Client, {firstname} {lastname}, was added.")
        client_id = cursor.lastrowid
        return client_id
    except ValueError as valueError:
        raise valueError
    except Exception as error:
        print(f"There was an error when adding the new client: {error}")
        connection.rollback()
        raise Exception('Registration failed')
    finally:
        cursor.close()
        connection.close()



def add_tradesperson(firstname, lastname, date_of_birth, task, town, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM clients where email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already exists on the client side. Please login using the client route or Sign up with a different email.")

        cursor.execute("SELECT COUNT(*) FROM tradespeople where email = %s", (email,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Email already exists")
        
        encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))
        insert = "INSERT INTO tradespeople (firstname, lastname, date_of_birth, taskID, townID, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (firstname, lastname, date_of_birth, task, town, email, encoded_password)
        cursor.execute(insert, values)
        connection.commit()
        print(f"Tradesperson, {firstname} {lastname}, was added.")
        worker_id = cursor.lastrowid
        return worker_id
    except ValueError as valueError:
        raise valueError
    except Exception as error:
        print(f"There was an error when adding the new tradesperson: {error}")
        connection.rollback()
        raise Exception('Registration failed')
    finally:
        cursor.close()
        connection.close()


def get_all_tradespeople():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_tradespeople_by_category;")
    workers = cursor.fetchall()
    return workers

def get_client_by_id(client_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clients WHERE clientID = %s"
    cursor.execute(query, (client_id,))
    client = cursor.fetchone()
    cursor.close()
    connection.close()
    return client

def get_client_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clients WHERE email = %s"
    cursor.execute(query, (email,))
    client = cursor.fetchone()
    cursor.close()
    connection.close()
    return client


def get_tp_by_id(workerID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM tradespeople WHERE workerID = %s"
    cursor.execute(query, (workerID,))
    tradesperson = cursor.fetchone()
    cursor.close()
    connection.close()
    return tradesperson


def get_tp_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM tradespeople WHERE email = %s"
    cursor.execute(query, (email,))
    tradesperson = cursor.fetchone()
    cursor.close()
    connection.close()
    return tradesperson



def get_all_towns():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT town FROM view_tradespeople_by_category")
    towns = cursor.fetchall()
    cursor.close()
    connection.close()
    return towns

def get_all_tasks():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT task_name FROM view_tradespeople_by_category")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks

def get_towns_with_ids():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT townID, town FROM location")
    towns = cursor.fetchall()
    cursor.close()
    connection.close()
    return towns

def get_tasks_with_ids():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT taskID, task_name FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks


def find_matching_tradespeople(task=None, location=None, hourly_rate=None, star_rating=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM view_tradespeople_by_category WHERE 1=1"
    search_parameters = []

    if task:
        query += " AND task_name = %s"
        search_parameters.append(task)
    
    if location:
        query += " AND town = %s"
        search_parameters.append(location)
    
    order = []
    if hourly_rate:
        order.append(f"hourly_rate {hourly_rate}")

    if star_rating:
        order.append(f"average_rating {star_rating}")

    if order:
        order += " ORDER BY " + ", ".join(order)

    cursor.execute(query, search_parameters)
    search_results = cursor.fetchall()
    cursor.close()
    connection.close()
    return search_results



def book_job(clientID, workerID, taskID, service_start, service_end, task_desc):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.callproc('BookJob', [clientID, workerID, taskID, service_start, service_end, task_desc])
        connection.commit()
        print(f"Booking successful: Client {clientID} booked worker {workerID} for task {taskID}.")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        cursor.close()
        connection.close()


def get_client_bookings(clientID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT bookingID, tp_full_name, task_name, booking_date, ss_date, se_date, task_description, status FROM view_past_bookings WHERE clientID = %s"
    cursor.execute(query, (clientID,))
    booking_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return booking_list


def get_booking_requests(workerID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT bookingID, booking_date, client_full_name, task_name, ss_date, se_date, working_days, task_description, status FROM view_booking_requests WHERE workerID = %s"
    cursor.execute(query, (workerID,))
    booking = cursor.fetchall()
    cursor.close()
    connection.close()
    return booking


def accept_booking_request(workerID, bookingID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    update = "UPDATE job_booking SET statusID = 2 WHERE workerID = %s AND bookingID = %s"
    cursor.execute(update, (workerID, bookingID))
    connection.commit()
    cursor.close()
    connection.close()


def reject_booking_request(workerID, bookingID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    update = "UPDATE job_booking SET statusID = 5 WHERE workerID = %s AND bookingID = %s"
    cursor.execute(update, (workerID, bookingID))
    connection.commit()
    cursor.close()
    connection.close()


def set_tp_profile(workerID, phone_number, hourly_rate, business, bio):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.callproc('set_tp_profile_info', [workerID, phone_number, hourly_rate, business, bio])
        connection.commit()
        print(f"Profile update was successful: Tradesperson {workerID} just updated their settings.")
    except Exception as error:
        print(f"An error occurredL: {error}")
    finally:
        cursor.close()
        connection.close()


def update_tradesperson_profile(workerID, phone_number, hourly_rate, business, bio):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_fields = []
    values = []

    if phone_number:
        update_fields.append("phone_number = %s")
        values.append(phone_number)

    if hourly_rate:
        update_fields.append("hourly_rate = %s")
        values.append(hourly_rate)

    if business:
        update_fields.append("business = %s")
        values.append(business)
    
    if bio:
        update_fields.append("bio = %s")
        values.append(bio)
    
    if update_fields:
        query = f"UPDATE tradesperson_profile SET {', '.join(update_fields)} WHERE workerID = %s"
        values.append(workerID)
        cursor.execute(query, tuple(values))
        connection.commit()
    cursor.close()
    connection.close()


def update_tp_personal_info(workerID, firstname=None, lastname=None, taskID=None, townID=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_fields = []
    values = []

    if firstname:
        update_fields.append("firstname = %s")
        values.append(firstname)

    if lastname:
        update_fields.append("lastname = %s")
        values.append(lastname)

    if taskID:
        update_fields.append("taskID = %s")
        values.append(taskID)
    
    if townID:
        update_fields.append("townID = %s")
        values.append(townID)
    
    if update_fields:
        query = "UPDATE tradespeople SET {', '.join(update_fields)} WHERE workerID = %s"
        values.append(workerID)
        print("Executing:", query)
        print("With values:", values)
        
        try:
            cursor.execute(query, tuple(values))
            connection.commit()
        except Exception as error:
            print("Database error:", error)
    else:
        print("No fields to update.")
    
    cursor.close()
    connection.close()


def display_tp_profile(workerID):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT full_name, task_name, town, hourly_rate, average_rating, total_reviews, bio, phone_number, business FROM view_tradespeople_by_category WHERE workerID = %s"
    cursor.execute(query, (workerID,))
    profile = cursor.fetchone()
    cursor.close()
    connection.close()
    return profile


def update_client_info(clientID, firstname=None, lastname=None, townID=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    update_fields = []
    values = []

    if firstname:
        update_fields.append("firstname = %s")
        values.append(firstname)

    if lastname:
        update_fields.append("lastname = %s")
        values.append(lastname)
    
    if townID:
        update_fields.append("townID = %s")
        values.append(townID)
    
    if update_fields:
        query = f"""
            UPDATE clients
            SET {', '.join(update_fields)}
            WHERE clientID = %s
        """
        values.append(clientID)
        print("Executing:", query)
        print("With values:", values)
        
        try:
            cursor.execute(query, tuple(values))
            connection.commit()
        except Exception as error:
            print("Database error:", error)
    else:
        print("No fields to update.")
    
    cursor.close()
    connection.close()


def display_client_profile(clientID):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT firstname, lastname, town, email FROM view_client_info WHERE clientID = %s"
    cursor.execute(query, (clientID,))
    profile = cursor.fetchone()
    cursor.close()
    connection.close()
    return profile


def get_reviews():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT full_name, task_name, rating, comment, town, rv_date FROM view_reviews")
    reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return reviews


def get_client_reviews(clientID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT rv_date, tp_full_name, task_name, town, rating, comment FROM view_personal_reviews WHERE clientID = %s"
    cursor.execute(query, (clientID,))
    client_reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return client_reviews

def get_tp_reviews(workerID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT rv_date, client_full_name, task_name, town, rating, comment FROM view_personal_reviews WHERE workerID = %s"
    cursor.execute(query, (workerID,))
    tp_reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return tp_reviews


def post_review(clientID, tp_profileID, rating, comment):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.callproc('post_review', [clientID, tp_profileID, rating, comment])
        connection.commit()
        print(f"Review by Client {clientID} for {tp_profileID} successfully posted!")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        cursor.close()
        connection.close()


def get_tp_profile():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT tp_profileID, tp_full_name FROM view_tp_profile ORDER BY firstname")
        tp_profile = cursor.fetchall()
        return tp_profile
    except Exception as error:
        print(f"Error fetching tradespeople: {error}")
        return []
    finally:
        cursor.close()
        connection.close()

# TO ENCODE THE PASSWORD OF CLIENTS
# client_passwords = [
#     ('miranda@gmail.com', 'Miranda123'),
#     ('nadine@gmail.com', 'Nadine123'),
#     ('liya@gmail.com', 'Liyaa123'),
#     ('malvina@gmail.com', 'Malvina123'),
#     ('ayishat@gmail.com', 'Ayishat123'),
#     ('ailsa@gmail.com', 'Ailsa123'),
#     ('angus@gmail.com', 'Angus123'),
#     ('kirsty@gmail.com', 'Kirsty123'),
#     ('rory@gmail.com', 'Roryy123'),
#     ('fiona@gmail.com', 'Fiona123'),
#     ('iain@gmail.com', 'Iainn123'),
#     ('skye@gmail.com', 'Skyee123'),
#     ('finlay@gmail.com', 'Finlay123'),
#     ('lachlan@gmail.com', 'Lachlan123'),
#     ('isla@gmail.com', 'islaa123'),
# ]

# mydb = get_db_connection()
# cursor = mydb.cursor()

# for email, password in client_passwords:
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

#     cursor.execute("""
#         UPDATE clients
#         SET password = %s
#         WHERE email = %s
#     """, (hashed_password, email))

# mydb.commit()
# cursor.close()
# mydb.close()

# print("Passwords updated successfully.")


# TO ENCODE THE PASSWORD OF TRADESPEOPLE
# tradespeople_passwords = [
#     ('lucy@edc.com', 'lucylack123'),
#     ('anita@edc.com', 'anita123'),
#     ('matt@nuwalls.com', 'mattfinish123'),
#     ('rick-@nuwalls.com', 'rickie123'),
#     ('annie@nodram.com', 'annie123'),
#     ('wett@nodram.com', 'stains123'),
#     ('wally@brushandhammer.com', 'wally123'),
#     ('paige@caseydecorating.com', 'paige123'),
#     ('hue@gtipainting.com', 'huehue123'),
#     ('dusty@dunbarpanting.com', 'dusty123'),
#     ('tessa@caseydecorating.com', 'tessa123'),
#     ('daisy@wcdecorators.com', 'daisy123'),
#     ('vinny@prodec.com', 'vinny123'),
#     ('gloria@grayandsons.com', 'gloria123'),
#     ('paula@swishdecorators.com', 'paula123'),
#     ('manny@grayandsons.com', 'manny123'),
#     ('penny@kingsburylawncare.com', 'penny123'),
#     ('chloe@acorngardening.com', 'chloe123'),
#     ('rosemary@bilawncare.com', 'rosemary123'),
#     ('chris@stewartgardening.com', 'chris123'),
#     ('jack@kingsburylawncare.com', 'jackie123'),
#     ('faye@edengardening.com', 'ferns123'),
#     ('hank@lieverlandscapes.com', 'hankie123'),
#     ('vera@bcstrees.com', 'vines123'),
#     ('luke@bcstrees.com', 'bushie123'),
#     ('Pat@greenthumbcarlisle.com', 'lawnie123'),
#     ('misty@humbiefencing.com', 'misty123'),
#     ('charlotte@groundcare.com', 'charlotte123'),
#     ('cameron@acorngardening.com', 'cameron123'),
#     ('poppy@wksolutions.com', 'poppy123'),
#     ('olive@gardenbros.com', 'olive123'),
#     ('tommy@mwgardening.com', 'tommy123'),
#     ('tinkles@flushbros.com', 'timmy123'),
#     ('peppa@flushbros.com', 'peppa123'),
#     ('david.dunn@upliftlogistics.com', 'david123'),
#     ('sean.hill@atlashaulers.com', 'sean123'),
#     ('sheila.mcintosh@packmasters.com', 'sheila123'),
#     ('kimberly.martin@titantransit.com', 'kimberly123'),
#     ('candace.thomas@rocketrelocations.com', 'candace123'),
#     ('nathan.garcia@boldmovehaulers.com', 'nathan123'),
#     ('seth.warner@silverlineshifters.com', 'seth123'),
#     ('rebecca.lane@silverlineshifters.com', 'rebecca123'),
#     ('monica.wolf@metromaxrelocations.com', 'monica123'),
#     ('danielle.collins@rocketrelocations.com', 'danielle123'),
#     ('nicole.west@firstclassfreight.com', 'nicole123'),
#     ('kaitlyn.rivera@anchorwavemovers.com', 'kaitlyn123'),
#     ('anthony.reed@boldmovehaulers.com', 'anthony123'),
#     ('bryan.barrett@urbantrekrelocations.com', 'bryan123'),
#     ('michael.rice@summithauling.com', 'michael123'),
#     ('daniel.deleon@urbantrekrelocations.com', 'daniel123'),
#     ('matthew.bray@peakpointmovers.com', 'matthew123'),
#     ('alice.wonderland@fixitpros.com', 'alice123'),
#     ('sarah.sky@skyhighrepairs.com', 'sarah123'),
#     ('tinatape@tapeitright.com', 'tina123'),
#     ('cindy.saw@sawmasters.com', 'cindy123'),
#     ('danny.drill@drillworks.com', 'danny123'),
#     ('ben.brick@brickbuilders.com', 'ben123'),
#     ('pat.paint@paintprodigy.com', 'pat123'),
#     ('dean.duct@ductdudes.com', 'dean123'),
#     ('info@clanelectrical.com', 'password!'),
#     ('hello@westrigg.com', 'sparkle123'),
#     ('contact@electroservices.com', 'plug4321'),
#     ('info@mcgowanelectrical.com', 'ME890!'),
#     ('hello@onedesignelectrical.com', 'Mal99!'),
#     ('contact@ces.com', 'current452'),
#     ('enquiry@BES.com', 'BES765490!'),
#     ('enquiries@elictrical.com', 'yjdyB1!!'),
#     ('mail@rodz.com', 'business5428'),
#     ('hi@calderwoodelectrical.com', 'caldelec12!'),
#     ('Pippa.Drains@homeheroes.co.uk', 'Pippa123'),
#     ('Lee Kay.Faucet@homeheroes.co.uk', 'Lee Kay123'),
#     ('Lou.Sinkler@homeheroes.co.uk', 'Lou123'),
#     ('Luke.Shower@homeheroes.co.uk', 'Luke123'),
#     ('Perry.Pipe@homeheroes.co.uk', 'Perry123'),
#     ('Flo.Stopcock@homeheroes.co.uk', 'Flo123'),
#     ('Mo.Taps@homeheroes.co.uk', 'Mo123'),
#     ('Sally.Plungerton@homeheroes.co.uk', 'Sally123'),
#     ('Ivana.Flush@homeheroes.co.uk', 'Ivana123'),
#     ('Bob.Boiler@homeheroes.co.uk', 'Bob123'),
#     ('Trudy.Trap@homeheroes.co.uk', 'Trudy123'),
#     ('Copper.Tubes@homeheroes.co.uk', 'Copper123'),
#     ('Billy.Backflow@homeheroes.co.uk', 'Billy123'),
#     ('Greta.Gasket@homeheroes.co.uk', 'Greta123'),
#     ('ValV.Pressure@homeheroes.co.uk', 'ValV123')
# ]

# mydb = get_db_connection()
# cursor = mydb.cursor()

# for email, password in tradespeople_passwords:
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

#     cursor.execute("""
#         UPDATE tradespeople
#         SET password = %s
#         WHERE email = %s
#     """, (hashed_password, email))

# mydb.commit()

# cursor.close()
# mydb.close()

# print("Tradespeople passwords updated successfully.")


def main():
    clientID = 2
    workerID = 1
    taskID = 1
    service_start = '2025-05-01'
    service_end = '2025-05-02'
    task_desc = "Paint the walls"

    book_job(clientID, workerID, taskID, service_start, service_end, task_desc)
    
    workerID = 5
    get_booking_requests(workerID)

if __name__ == '__main__':
    main()

    
if __name__ == '__main__':
    print("Tasks test:", get_tasks_with_ids())
    print("Towns test:", get_towns_with_ids())
    print(get_client_by_email("nadine@gmail.com"))
    print(get_tp_profile())
