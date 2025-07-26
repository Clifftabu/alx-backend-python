#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches from the user_data table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tabucliff12!',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(
                f"SELECT * FROM user_data ORDER BY user_id LIMIT {batch_size} OFFSET {offset}"
            )
            rows = cursor.fetchall()
            if not rows:
                break
            for row in rows:
                yield row
            offset += batch_size

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """Returns a list of users over the age of 25."""
    users_over_25 = []

    for user in stream_users_in_batches(batch_size):
        if user['age'] > 25:
            users_over_25.append(user)

    return users_over_25
