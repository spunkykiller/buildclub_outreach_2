import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT body_formal FROM emails WHERE author_id = (SELECT id FROM authors WHERE full_name = 'Derek Sivers')")
    res = cursor.fetchone()
    if res:
        print("Email Content for Derek Sivers:")
        print("-" * 20)
        print(res[0])
        print("-" * 20)
    else:
        print("No email found for Derek Sivers")
    conn.close()

if __name__ == "__main__":
    verify()
