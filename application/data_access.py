import mysql.connector
import bcrypt
import sys

if sys.platform == "win32":
    mysql_password = "password"
else:
    mysql_password = ""

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="password",
#   database="homeheroes1"
# )


def get_tradespeopledb_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="homeheroes1"
    )
    return mydb

def add_client(firstname, lastname, date_of_birth, email, password):
    conn = get_tradespeopledb_connection()
    cursor = conn.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO clients (firstname, lastname, date_of_birth, email, password, registration_date) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE())"
    val = (firstname, lastname, date_of_birth, email, encoded_password)
    cursor.execute(sql, val)
    conn.commit()

    print(f"Client, {firstname} {lastname}, was added.")

def add_tradesperson(firstname, lastname, date_of_birth, profession, town, email, password):
    conn = get_tradespeopledb_connection()
    cursor = conn.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO tradespeople (firstname, lastname, date_of_birth, profession, town, email, password, registration_date) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE())"
    val = (firstname, lastname, date_of_birth, profession, town, email, encoded_password)
    cursor.execute(sql, val)
    conn.commit()

    print(f"Tradesperson, {firstname} {lastname}, was added.")


def get_client():
    conn = get_tradespeopledb_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        


""")

def get_tradesperson():
    pass

if __name__ == "__main__":
    main()