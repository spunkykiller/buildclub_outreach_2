import sqlite3
import os
import urllib.request
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

def check_db():
    print("Checking Database...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check for Jason Cohen
    cursor.execute("SELECT full_name, detailed_description, bio, context, linkedin FROM authors WHERE full_name LIKE '%Jason Cohen%'")
    row = cursor.fetchone()
    if row:
        print(f"DB Row for Jason Cohen: {dict(row)}")
    else:
        print("Jason Cohen not found in DB")
        
    # Check count of non-null bios/descriptions
    cursor.execute("SELECT count(*) FROM authors WHERE detailed_description IS NOT NULL OR bio IS NOT NULL")
    count = cursor.fetchone()[0]
    print(f"Authors with description/bio: {count}")
    
    conn.close()

def check_api():
    print("\nChecking API...")
    try:
        with urllib.request.urlopen("http://localhost:8001/authors") as response:
            data = json.load(response)
            if data:
                print(f"First API Author: {data[0]}")
                # Find Jason Cohen in API response
                jason = next((a for a in data if "Jason Cohen" in a['full_name']), None)
                if jason:
                     print(f"API Entry for Jason Cohen: {jason}")
                else:
                    print("Jason Cohen not found in API response")
            else:
                print("API returned empty list")
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    check_db()
    check_api()
