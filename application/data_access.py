import mysql.connector
import bcrypt
import sys

# if sys.platform == "win32":
#     mysql_password = "password"
# else:
#     mysql_password = ""

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="homeheroes2"
)

def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="homeheroes2"
    )
    return mydb


def add_client(firstname, lastname, date_of_birth, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO clients (firstname, lastname, date_of_birth, email, password) VALUES (%s, %s, %s, %s, %s)"
    val = (firstname, lastname, date_of_birth, email, encoded_password)
    cursor.execute(sql, val)
    connection.commit()

    print(f"Client, {firstname} {lastname}, was added.")


def add_tradesperson(firstname, lastname, date_of_birth, task, town, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO tradespeople (firstname, lastname, date_of_birth, taskID, townID, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (firstname, lastname, date_of_birth, task, town, email, encoded_password)
    cursor.execute(sql, val)
    connection.commit()

    print(f"Tradesperson, {firstname} {lastname}, was added.")


def get_all_tradespeople():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM view_tradespeople_by_category;")
    workers = cursor.fetchall()
    return workers


def get_client_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM clients WHERE email = %s"
    cursor.execute(query, (email,))
    client = cursor.fetchone()

    cursor.close()
    connection.close()
    return client


def get_tp_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM tradespeople WHERE email = %s"
    cursor.execute(query, (email,))
    tradesperson = cursor.fetchone()

    cursor.close()
    connection.close()
    return tradesperson
    


def book_job(clientID, workerID, taskID, service_start, service_end, townID, task_desc):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.callproc('BookJob', [clientID, workerID, taskID, service_start, service_end, townID, task_desc])

    connection.commit()
    cursor.close()
    connection.close()

def get_booking():
    pass


if __name__ == "__main__":
    main()