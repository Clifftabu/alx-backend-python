# setup_db.py
import sqlite3

# Create and connect to users.db
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Add some test users
cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alicekamau@gmail.com')")
cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bobnjagi@gmail.com')")
conn.commit()

# Close the connection
conn.close()

print("Database and table set up successfully.")
