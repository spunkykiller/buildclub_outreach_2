import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sqlite3
import logging
from backend.db import get_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "google_creds.json")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Outreach Tracker")

class SheetSyncer:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.client = None
        self.sheet = None

    def connect(self):
        try:
            if not os.path.exists(CREDENTIALS_FILE):
                logging.warning(f"Google credentials file not found at {CREDENTIALS_FILE}. Sync disabled.")
                return False
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, self.scope)
            self.client = gspread.authorize(creds)
            try:
                self.sheet = self.client.open(SHEET_NAME).sheet1
            except gspread.SpreadsheetNotFound:
                logging.info(f"Sheet '{SHEET_NAME}' not found. Creating it...")
                sh = self.client.create(SHEET_NAME)
                # Helper: Share with self (Zoho email)
                try:
                    sh.share(os.getenv("ZOHO_EMAIL"), perm_type='user', role='writer')
                    logging.info(f"Shared sheet with {os.getenv('ZOHO_EMAIL')}")
                except:
                    pass
                self.sheet = sh.sheet1
                self.sheet.append_row(["Name", "Company", "Book", "Email", "Status", "Last Contact", "Personalization Summary", "Source", "Notes"])
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Google Sheets: {e}")
            return False

    def sync_db_to_sheet(self):
        if not self.client and not self.connect():
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch authors where we haven't confirmed sync or just all pending
        # Improved logic: Sync those not marked 'added_to_sheet' in pipeline
        cursor.execute("""
            SELECT a.id, a.full_name, a.company, b.title as book_title, a.email, 
                   e.status, e.last_sent_at, an.philosophy, a.source_url
            FROM authors a
            LEFT JOIN books b ON a.id = b.author_id
            LEFT JOIN emails e ON a.id = e.author_id
            LEFT JOIN analysis an ON a.id = an.author_id
            LEFT JOIN pipeline_status p ON a.id = p.author_id
            WHERE p.added_to_sheet = 0 OR p.added_to_sheet IS NULL
        """)
        rows = cursor.fetchall()
        
        try:
            for row in rows:
                if not row['email']: continue
                
                self.sheet.append_row([
                    row['full_name'],
                    row['company'] or "",
                    row['book_title'] or "",
                    row['email'],
                    row['status'] or "discovered",
                    str(row['last_sent_at']) if row['last_sent_at'] else "",
                    (row['philosophy'][:50] + "...") if row['philosophy'] else "",
                    row['source_url'] or "",
                    ""
                ])
                logging.info(f"Synced {row['full_name']} to Sheet.")
                
                # Mark as synced
                # We need a new cursor for commit or use same connection
                conn.execute("""
                    INSERT INTO pipeline_status (author_id, added_to_sheet) VALUES (?, 1)
                    ON CONFLICT(author_id) DO UPDATE SET added_to_sheet=1
                """, (row['id'],))
                
            conn.commit()
                    
        except Exception as e:
            logging.error(f"Sync error: {e}")
        
        conn.close()
