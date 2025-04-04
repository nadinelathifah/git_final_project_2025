import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sign"
)


def get_signupdb_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sign"
    )
    return mydb


if __name__ == "__main__":
    main()