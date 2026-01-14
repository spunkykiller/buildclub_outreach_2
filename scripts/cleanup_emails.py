import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

def cleanup():
    conn = sqlite3.connect(DB_PATH)
    # Delete emails with podcast variant
    conn.execute("DELETE FROM emails WHERE selected_variant='podcast'")
    # Reset pipeline status for manually uploaded leads
    conn.execute("UPDATE pipeline_status SET email_generated=0 WHERE author_id IN (SELECT id FROM authors WHERE discovery_status='manual_upload')")
    conn.commit()
    conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
