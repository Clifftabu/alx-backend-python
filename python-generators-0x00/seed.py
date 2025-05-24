import mysql.connector
import csv
import uuid
from mysql.connector import Error
from contextlib import contextmanager

def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='Tabucliff12!'   # replace with your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # replace with your MySQL username
            password='Tabucliff12!',  # replace with your MySQL password
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,0) NOT NULL,
            INDEX (user_id)
        )
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()


# Modify 
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file) as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Generate UUID for each row
                user_id = str(uuid.uuid4())
                cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        print("Data inserted with generated UUIDs")
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()

# Generator function to stream rows one by one
def stream_users(connection):
    """Generator that yields rows from user_data one at a time"""
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()