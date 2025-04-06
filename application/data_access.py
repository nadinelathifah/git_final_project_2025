import mysql.connector
import bcrypt

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="tradespeopledb"
)


def get_tradespeopledb_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tradespeopledb"
    )
    return mydb

def add_client(firstname, lastname, email, password):
    conn = get_tradespeopledb_connection()
    cursor = conn.cursor()

    encoded_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt(12))

    sql = "INSERT INTO clients (firstname, lastname, email, password) VALUES (%s %s %s %s)"
    val = (firstname, lastname, email, encoded_password)
    cursor.execute(sql, val)
    conn.commit()

    print(f"Client, {firstname} {lastname}, was added.")

def add_tradesperson():
    pass

def get_client():
    pass

def get_tradesperson():
    pass

if __name__ == "__main__":
    main()