#  Memory-Efficient Aggregation with Generators
seed = __import__('seed')

def stream_user_ages():
    """
    Generator that yields user ages from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data")
    rows = cursor.fetchall()

    for row in rows:
        yield row
    connection.close()
    return rows


def calculate_avg_age():
    count = 0
    ages = 0
    values = stream_user_ages()

    for val in values:
        ages += int(val['age'])
        count += 1

    avg_age = ages // count
    print(f"Average age of users: {avg_age}")

calculate_avg_age()

