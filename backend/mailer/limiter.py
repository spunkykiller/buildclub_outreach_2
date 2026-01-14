import time
import os
import sqlite3
from pathlib import Path

# Use a lock file in the temp or project dir
LOCK_FILE = Path("sender.lock")
DB_PATH = os.getenv("DB_PATH", "local_system.db")
RATE_LIMIT = int(os.getenv("RATE_LIMIT_SECONDS", 3600))

from backend.db import get_connection

class RateLimiter:
    def __init__(self):
        pass

    def can_send(self):
        """
        Checks if we can send an email right now.
        Rules:
        1. No other process is sending (Lock file).
        2. Last email sent > 1 hour ago.
        """
        if LOCK_FILE.exists():
            # Check if stale (older than 5 mins)
            if time.time() - LOCK_FILE.stat().st_mtime > 300:
                print("Removing stale lock file.")
                LOCK_FILE.unlink()
            else:
                print("Locked by another process.")
                return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sent_at FROM sends ORDER BY sent_at DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            last_sent_str = row[0]
            # Parse timestamp (SQLite stores as string typically YYYY-MM-DD HH:MM:SS)
            # We can use time.mktime or simple string comparison if confident, 
            # but safer to let SQLite 'julianday' or python database adapters handle it.
            # Assuming standard SQLite timestamp format:
            # We'll use sql function to check difference to be safe/easy on format.
            return self._check_db_time_diff()
        
        return True

    def _check_db_time_diff(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Check if any email sent in last hour
        cursor.execute(f"SELECT 1 FROM sends WHERE sent_at > datetime('now', '-{RATE_LIMIT} seconds')")
        recent = cursor.fetchone()
        conn.close()
        if recent:
            print("Rate limit hit: Email sent recently.")
            return False
        return True

    def acquire_lock(self):
        LOCK_FILE.touch()

    def release_lock(self):
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
