import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sqlite3
import random
import time
from .limiter import RateLimiter
from backend.db import get_connection

ZOHO_EMAIL = os.getenv("ZOHO_EMAIL")
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")
SMTP_SERVER = "smtp.zoho.in"
SMTP_PORT = 587

class Mailer:
    def __init__(self):
        self.limiter = RateLimiter()

    def send_next_queued_email(self):
        if not self.limiter.can_send():
            return False

        conn = get_connection()
        cursor = conn.cursor()

        # Get next pending email
        cursor.execute("""
            SELECT e.author_id, e.subject, e.body_formal, e.body_friendly, e.body_short, e.selected_variant,
                   a.email, a.full_name
            FROM emails e
            JOIN authors a ON e.author_id = a.id
            WHERE e.status = 'pending' AND a.email IS NOT NULL NOT IN (SELECT email FROM blacklist)
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        
        if not row:
            print("No pending emails to send.")
            conn.close()
            return False

        variant = row['selected_variant']
        body = row[f'body_{variant}']
        
        self.limiter.acquire_lock()
        success = False
        try:
            self._send_via_smtp(row['email'], row['subject'], body)
            success = True
            print(f"Email sent to {row['email']}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            self.limiter.release_lock()

        # Update DB
        status = 'sent' if success else 'failed'
        cursor.execute("UPDATE emails SET status = ?, last_sent_at = CURRENT_TIMESTAMP WHERE author_id = ?", (status, row['author_id']))
        if success:
            cursor.execute("INSERT INTO sends (author_id, email_sent_to, status) VALUES (?, ?, ?)", 
                           (row['author_id'], row['email'], 'success'))
            
            # Update Pipeline
            cursor.execute("""
                INSERT INTO pipeline_status (author_id, sent) VALUES (?, 1)
                ON CONFLICT(author_id) DO UPDATE SET sent=1
            """, (row['author_id'],))
        
        conn.commit()
        conn.close()
        return success

    def _send_via_smtp(self, to_email, subject, body):
        message = MIMEMultipart()
        message["From"] = ZOHO_EMAIL
        message["To"] = to_email
        message["Subject"] = subject
        
        if body.startswith("Subject:"):
            lines = body.split("\n")
            subject = lines[0].replace("Subject:", "").strip()
            body = "\n".join(lines[1:]).strip()
            message["Subject"] = subject
        
        footer = "\n\n--\nTo opt-out of future emails, please reply 'UNSUBSCRIBE'."
        body += footer

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(ZOHO_EMAIL, ZOHO_PASSWORD)
            server.send_message(message)
