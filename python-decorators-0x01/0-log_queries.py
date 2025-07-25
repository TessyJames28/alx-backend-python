import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""
def log_queries(func):
    """Decorator to log queries executed by a function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time = datetime.now()
        query = kwargs.get("query") or (args[0] if args else "UNKWOWN QUERY")
        result = func(*args, **kwargs)
        print(f"[{time}] Executing query: {query}")
        return result
    return wrapper 



@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")