import sqlite3
import os

# Get absolute path to users.db from the current file
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-decorators-0x01', 'users.db'))

class DatabaseConnection:
    """Class to automatically opena and close db connection"""
    def __init__(self):
        self.conn = sqlite3.connect(db_path)

    def __enter__(self):
        return self.conn
    
    def __exit__(self, type, value, traceback):
        self.conn.close()