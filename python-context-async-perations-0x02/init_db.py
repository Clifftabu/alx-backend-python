import sqlite3

def setup_database():
    conn = sqlite3.connect("users.db")  # This creates 'users.db' in the current folder
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    
    cursor.executemany(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 22),
            ("Diana", 50),
            ("Eve", 27),
        ]
    )

    conn.commit()
    conn.close()
    print("✅ users.db created and populated.")

if __name__ == "__main__":
    setup_database()
