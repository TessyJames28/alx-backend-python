# Objective: create a generator that streams rows from an SQL
# database one by one.

import sqlite3
import os, csv


def connect_db():
    """Connect to the Sqlite database."""
    try:
        connection = sqlite3.connect("users.db")
        print("Server connection successful")
        return connection
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """
    creates a table user_data if it does not exists with
    the required fields
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)")
    connection.commit()
    cursor.close()


def insert_data(connection, data):
    print(f"insert_data: {data} is of type {type(data)}")
    print("CSV exists:", os.path.isfile(data), "| Path:", data)

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

                    # Check for duplicates by email
                    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO users (name, email, age)
                            VALUES (?, ?, ?)
                        """, (name.strip(), email.strip(), age.strip()))
                        inserted += 1

                connection.commit()
                print(f"{inserted} users inserted from CSV.")

        except Exception as e:
            print("Error reading CSV:", e)
        finally:
            cursor.close()
    else:
        print("insert_data: CSV file not found or invalid input.")

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_table(conn)
        insert_data(conn, "user_data.csv")
        conn.close()
