# create a generator that streams rows from an SQL database
# one by one.
seed = __import__('seed')

def stream_users():
    """
    write a function that uses a generator to fetch rows one
    by one from the user_data table.
    """
    connection = seed.connect_db()
    if connection:
        print(f"connection successful")
        connection = seed.connect_to_prodev()

        if connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM user_data;")
            result = cursor.fetchall()
            output = {}
            for row in result:
                output['user_id'] = row[0]
                output['name'] = row[1]
                output['email'] = row[2]
                output['age'] = row[3]
                yield output