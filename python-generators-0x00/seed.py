# Objective: create a generator that streams rows from an SQL
# database one by one.

import mysql.connector
import uuid, os, csv


def connect_db():
    """Connect to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gemini285#",
        )
        print("Server connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_database(connection):
    """creates the database ALX_prodev if it does not exist"""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    """connects the the ALX_prodev database in MYSQL"""
    conn = connect_db()
    if conn is None:
        return None
    create_database(conn)

    # Reconnect and select ALX_prodev database
    conn.database = "ALX_prodev"

    return conn


def create_table(connection):
    """
    creates a table user_data if it does not exists with
    the required fields
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()


def insert_data(connection, data):
    print(f"insert_data: {data} is of type {type(data)}")
    """
    Inserts data into the database.

    If data is a string (e.g., 'user_data.csv'), it treats it as a CSV path and inserts rows.
    """
    if isinstance(data, str) and os.path.isfile(data):
        cursor = connection.cursor()
        try:
            with open(data, newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)  # skip header
                inserted = 0

                for row in reader:
                    if len(row) != 3:
                        continue  # skip malformed rows

                    name, email, age = row
                    uid = str(uuid.uuid4())

                    # Check for duplicates by email
                    cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (email,))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO user_data (user_id, name, email, age)
                            VALUES (%s, %s, %s, %s)
                        """, (uid, name.strip(), email.strip(), age.strip()))
                        inserted += 1

                connection.commit()
                print(f"{inserted} users inserted from CSV.")

        except Exception as e:
            print("Error reading CSV:", e)
        finally:
            cursor.close()
    else:
        print("insert_data: CSV file not found or invalid input.")

