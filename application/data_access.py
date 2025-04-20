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

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    insert = "INSERT INTO clients (firstname, lastname, date_of_birth, townID, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (firstname, lastname, date_of_birth, town, email, encoded_password)
    cursor.execute(insert, values)
    connection.commit()

    print(f"Client, {firstname} {lastname}, was added.")


def add_tradesperson(firstname, lastname, date_of_birth, task, town, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    insert = "INSERT INTO tradespeople (firstname, lastname, date_of_birth, taskID, townID, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (firstname, lastname, date_of_birth, task, town, email, encoded_password)
    cursor.execute(insert, values)
    connection.commit()

    print(f"Tradesperson, {firstname} {lastname}, was added.")


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
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()


def get_client_bookings(clientID):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT tp_full_name, task_name, booking_date, ss_date, se_date, task_description, status FROM view_past_bookings WHERE clientID = %s"
    cursor.execute(query, (clientID,))
    booking_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return booking_list



def set_tp_profile(workerID, phone_number, hourly_rate, business, bio):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.callproc('set_tp_profile_info', [workerID, phone_number, hourly_rate, business, bio])
        connection.commit()
        print(f"Profile update was successful: Tradesperson {workerID} just updated their settings.")
    except Exception as e:
        print(f"An error occurredL: {e}")
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
        query = f"""
            UPDATE tradespeople
            SET {', '.join(update_fields)}
            WHERE workerID = %s
        """
        values.append(workerID)
        print("Executing:", query)
        print("With values:", values)
        
        try:
            cursor.execute(query, tuple(values))
            connection.commit()
        except Exception as e:
            print("Database error:", e)
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
        except Exception as e:
            print("Database error:", e)
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

    cursor.execute("SELECT rating, full_name, comment FROM view_reviews")
    reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return reviews


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
#     ('anita@edc.com', 'anita123')
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

if __name__ == '__main__':
    main()

    
if __name__ == '__main__':
    print("Tasks test:", get_tasks_with_ids())
    print("Towns test:", get_towns_with_ids())
