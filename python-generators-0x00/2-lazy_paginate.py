# Simulate fetching paginated data from the users database
# using a generator to lazily load each page
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Function that only only fetch the next page when needed
    at an offset of 0.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches users in pages of size page_size.
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        
        page = []
        for row in rows:
            output = {
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            }
            page.append(output.copy())
            
            yield page
        offset += page_size