import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

def check():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, detailed_description, bio FROM authors WHERE full_name LIKE 'Arvid Kahl%'")
    row = cursor.fetchone()
    if row:
        print(f"Data for Arvid Kahl: {dict(row)}")
    else:
        print("Arvid Kahl not found")
    conn.close()

if __name__ == "__main__":
    check()
