# Create a generator to fetch and process data in batches
# from the users database
seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """Function that fetches user rows in batches"""
    connection = seed.connect_db()
    if connection:
        print(f"connection successful")
        connection = seed.connect_to_prodev()

        if connection:
            cursor = connection.cursor()
            offset = 0
            while True:
                cursor.execute(f"SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
                rows = cursor.fetchall()

                if not rows:
                    break

                output = {}
                for row in rows:
                    output['user_id'] = row[0]
                    output['name'] = row[1]
                    output['email'] = row[2]
                    output['age'] = row[3]
                    yield output


def batch_processing(batch_size):
    """
    Function that processes each batch to filter users 
    over the age of 25
    """
    print("Called this function")
    for user in stream_users_in_batches(batch_size):
        print(f"Processing user: {user['name']} with age {user['age']}")
        if user['age'] > 25:
            print(user)