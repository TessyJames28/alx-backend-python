import sqlite3
import os

# Get absolute path to users.db from the current file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-decorators-0x01', 'users.db'))

class ExecuteQuery:
    """
    Class to automatically open and close db connection
    As well as execute query
    """
    def __init__(self, age=0):
        self.conn = sqlite3.connect(db_path)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.conn.close()

    def execute(self, query, age=0):
        """Method to execute sql query"""
        cursor = self.conn.cursor()
        cursor.execute(query, (age,))
        return cursor.fetchall()



with ExecuteQuery() as db:
    users= db.execute("SELECT * FROM users WHERE age > ?", 25)
    print(users)