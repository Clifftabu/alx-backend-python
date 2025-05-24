import sqlite3

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()


# Testing to be done
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
