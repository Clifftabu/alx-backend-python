#!/usr/bin/python3


import mysql.connector
from mysql.connector import Error


def stream_user_ages():
   
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Tabucliff12!',  # Update with your password
            database='ALX_prodev',
            auth_plugin='Tabucliff12!'

        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Yield each age one by one (Loop 1)
        for row in cursor:
            yield row[0]  # row[0] contains the age value
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def calculate_average_age():
   
    total_age = 0
    count = 0
    
    # Use the generator to process ages one by one (Loop 2)
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


if __name__ == "__main__":
    # Calculate and print the average age
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age}")