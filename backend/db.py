import sqlite3
import os
from pathlib import Path
import logging

# Set DB_PATH relative to project root (one level up from backend) usually, 
# but for simplicity let's keep it in the root "local_system.db"
# Since we are running from 'backend' or root, let's be robust.
ROOT_DIR = Path(__file__).parent.parent
DB_PATH = os.getenv("DB_PATH", str(ROOT_DIR / "local_system.db"))

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    try:
        # Enable FKs
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Authors
        conn.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                company TEXT,
                industry TEXT,
                website TEXT,
                email TEXT UNIQUE,
                linkedin TEXT,
                country TEXT,
                source_url TEXT,
                discovery_status TEXT DEFAULT 'new',
                detailed_description TEXT,
                response_probability INTEGER,
                context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Schema Migration for existing tables
        _migrate_authors_table(conn)

        # Books
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER,
                title TEXT,
                year INTEGER,
                pdf_path TEXT,
                analysis_status TEXT DEFAULT 'pending',
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        """)

        # Analysis
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                author_id INTEGER PRIMARY KEY,
                philosophy TEXT,
                principles TEXT,
                tone TEXT,
                beliefs TEXT,
                opportunities TEXT,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        """)

        # Emails
        conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                author_id INTEGER PRIMARY KEY,
                subject TEXT,
                body_formal TEXT,
                body_friendly TEXT,
                body_short TEXT,
                selected_variant TEXT,
                status TEXT DEFAULT 'pending', 
                last_sent_at TIMESTAMP,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        """)

        # Pipeline Status (New)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_status (
                author_id INTEGER PRIMARY KEY,
                discovered BOOLEAN DEFAULT 0,
                pdf_uploaded BOOLEAN DEFAULT 0,
                analyzed BOOLEAN DEFAULT 0,
                email_generated BOOLEAN DEFAULT 0,
                added_to_sheet BOOLEAN DEFAULT 0,
                sent BOOLEAN DEFAULT 0,
                connection_sent BOOLEAN DEFAULT 0,
                dm_sent BOOLEAN DEFAULT 0,
                response_status TEXT,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        """)
        
        # Migrate Pipeline table (New)
        _migrate_pipeline_table(conn)

        # Logs (New)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event TEXT,
                author_id INTEGER,
                level TEXT
            )
        """)

        # Blacklist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS blacklist (
                email TEXT PRIMARY KEY,
                reason TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sends Log
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id INTEGER,
                email_sent_to TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        """)

        conn.commit()
        logging.info("Database initialized with enhanced schema.")
    except Exception as e:
        logging.error(f"Error initializing DB: {e}")
    finally:
        conn.close()

def _migrate_pipeline_table(conn):
    """Ensure new columns exist in pipeline_status table"""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(pipeline_status)")
    columns = [row[1] for row in cursor.fetchall()]
    
    new_cols = {
        "connection_sent": "BOOLEAN DEFAULT 0",
        "dm_sent": "BOOLEAN DEFAULT 0",
        "response_status": "TEXT"
    }
    
    for col_name, col_type in new_cols.items():
        if col_name not in columns:
            try:
                logging.info(f"Migrating pipeline_status table: adding {col_name}")
                conn.execute(f"ALTER TABLE pipeline_status ADD COLUMN {col_name} {col_type}")
            except Exception as e:
                logging.error(f"Failed to add column {col_name}: {e}")
    conn.commit()


def _migrate_authors_table(conn):
    """Ensure new columns exist in authors table"""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(authors)")
    columns = [row[1] for row in cursor.fetchall()]
    
    new_cols = {
        "detailed_description": "TEXT",
        "response_probability": "INTEGER",
        "context": "TEXT"
    }
    
    for col_name, col_type in new_cols.items():
        if col_name not in columns:
            try:
                logging.info(f"Migrating authors table: adding {col_name}")
                conn.execute(f"ALTER TABLE authors ADD COLUMN {col_name} {col_type}")
            except Exception as e:
                logging.error(f"Failed to add column {col_name}: {e}")
    conn.commit()

def log_event(author_id, event, level="INFO"):
    try:
        conn = get_connection()
        conn.execute("INSERT INTO logs (event, author_id, level) VALUES (?, ?, ?)", 
                     (event, author_id, level))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log event: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
