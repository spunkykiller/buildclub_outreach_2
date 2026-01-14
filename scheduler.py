import time
import schedule
import logging
from discovery.scraper import DiscoveryEngine
from analysis.analyzer import PDFAnalyzer
from email_engine.generator import EmailGenerator
from mailer.sender import Mailer
from sheets.syncer import SheetSyncer
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_discovery_task():
    try:
        logging.info("Starting scheduled Discovery task...")
        # Since discovery is async, we need a runner
        engine = DiscoveryEngine()
        asyncio.run(engine.run_discovery())
    except Exception as e:
        logging.error(f"Discovery task failed: {e}")

def run_analysis_task():
    try:
        logging.info("Starting scheduled Analysis task...")
        analyzer = PDFAnalyzer()
        analyzer.scan_and_analyze()
    except Exception as e:
        logging.error(f"Analysis task failed: {e}")

def run_email_gen_task():
    try:
        logging.info("Starting scheduled Email Generation task...")
        generator = EmailGenerator()
        generator.generate_emails_for_pending_authors()
    except Exception as e:
        logging.error(f"Email Generation task failed: {e}")

def run_mailer_task():
    try:
        # Mailer is rate limited, check every minute is fine
        mailer = Mailer()
        sent = mailer.send_next_queued_email()
        if sent:
            logging.info("Mail task sent an email.")
    except Exception as e:
        logging.error(f"Mailer task failed: {e}")

def run_sync_task():
    try:
        logging.info("Starting Google Sheets Sync...")
        syncer = SheetSyncer()
        syncer.sync_db_to_sheet()
    except Exception as e:
        logging.error(f"Sync task failed: {e}")

def main():
    logging.info("Starting Local Automation Scheduler...")
    
    # Schedule tasks
    
    # Discovery: Every 24 hours
    schedule.every(24).hours.do(run_discovery_task)
    
    # Analysis: Every 1 hour (check for new files)
    schedule.every(1).hours.do(run_analysis_task)
    
    # Email Generation: Every 1 hour
    schedule.every(1).hours.do(run_email_gen_task)
    
    # Mailer: Check every 5 minutes (Limiter handles the 1/hr logic)
    # We check frequently so if one hour passes, we send ASAP.
    schedule.every(5).minutes.do(run_mailer_task)
    
    # Sheets Sync: Every 30 minutes
    schedule.every(30).minutes.do(run_sync_task)
    
    # Initial run of watchers (Optional, maybe too heavy on startup)
    # run_analysis_task()
    # run_email_gen_task()
    
    logging.info("Scheduler running. Press Ctrl+C to exit.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
