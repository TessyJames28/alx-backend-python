import time
import sqlite3 
import functools

with_db_connection = __import__('1-with_db_connection').with_db_connection

#### paste your with_db_decorator here
def retry_on_failure(retries=3, delay=2):
    """Decorator that retries the function a certain num of times"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            conn = args[0] if args else kwargs.get("conn")
            while attempt < retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    attempt += 1
                    if attempt < retries:
                        time.sleep(delay)
        return wrapper
    return decorator
            


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)