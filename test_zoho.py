import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv("config.env")

ZOHO_EMAIL = os.getenv("ZOHO_EMAIL")
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")
TO_EMAIL = "mohitsilla12@gmail.com"

def send_test_email():
    print(f"Sending test email from {ZOHO_EMAIL} to {TO_EMAIL}...")
    msg = EmailMessage()
    msg["From"] = ZOHO_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Test Email from Local Automation System"
    msg.set_content("Hi\n\nThis is a test email from the local automation system.")

    try:
        # Trying smtp.zoho.in as domain is .in
        print("Trying smtp.zoho.in...")
        with smtplib.SMTP("smtp.zoho.in", 587) as server:
            server.starttls()
            server.login(ZOHO_EMAIL, ZOHO_PASSWORD)
            server.send_message(msg)
        print("[OK] Email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to send: {e}")

if __name__ == "__main__":
    send_test_email()
