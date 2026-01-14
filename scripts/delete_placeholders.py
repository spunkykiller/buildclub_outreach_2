import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

def cleanup():
    print(f"Connecting to {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Delete Niche Founders
    cursor.execute("DELETE FROM authors WHERE full_name LIKE 'Niche Founder%'")
    deleted_authors = cursor.rowcount
    print(f"Deleted {deleted_authors} placeholder authors.")
    
    # 2. Cleanup orphaned emails
    cursor.execute("DELETE FROM emails WHERE author_id NOT IN (SELECT id FROM authors)")
    print(f"Deleted {cursor.rowcount} orphaned emails.")
    
    # 3. Cleanup orphaned pipeline_status
    cursor.execute("DELETE FROM pipeline_status WHERE author_id NOT IN (SELECT id FROM authors)")
    print(f"Deleted {cursor.rowcount} orphaned pipeline statuses.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    cleanup()
