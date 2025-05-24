#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams users one by one from database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tabucliff12!',
            database='ALX_prodev',
            auth_plugin='Tabucliff12!'

        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()