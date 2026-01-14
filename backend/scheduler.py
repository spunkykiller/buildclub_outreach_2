from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from .discovery.scraper import DiscoveryEngine
from .analysis.analyzer import PDFAnalyzer
from .email_engine.generator import EmailGenerator
from .mailer.sender import Mailer
from .sheets.syncer import SheetSyncer

# Since scraper is async, we wrap it? 
# Appscheduler matches asyncio.
import asyncio

logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler()

async def discovery_job():
    # Discovery usually needs a query. 
    # For automated background, we might check a queue or just run a default "maintenance" crawl?
    # Or skip discovery in auto-loop and only keep explicit trigger.
    # Let's verify discovery is mainly manual trigger via UI.
    pass 

def analysis_job():
    # Analyzer uses sync fitz, requests. Safe to run in executor or just run?
    # Fastapi handles it.
    try:
        logging.info("Running Analysis Job...")
        PDFAnalyzer().scan_and_analyze()
    except Exception as e:
        logging.error(f"Analysis Job failed: {e}")

def generation_job():
    try:
        logging.info("Running Generator Job...")
        EmailGenerator().generate_emails_for_pending_authors()
    except Exception as e:
        logging.error(f"Generator Job failed: {e}")

def mailer_job():
    try:
        # Mailer checks rate limit itself
        Mailer().send_next_queued_email()
    except Exception as e:
        logging.error(f"Mailer Job failed: {e}")

def sync_job():
    try:
        SheetSyncer().sync_db_to_sheet()
    except Exception as e:
        logging.error(f"Sync Job failed: {e}")

def start_scheduler():
    # Schedule Analysis (Every 10 mins)
    scheduler.add_job(analysis_job, IntervalTrigger(minutes=10))
    
    # Schedule Generation (Every 10 mins)
    scheduler.add_job(generation_job, IntervalTrigger(minutes=10))
    
    # Schedule Mailer (Disabled per user request)
    # scheduler.add_job(mailer_job, IntervalTrigger(minutes=5))
    
    # Schedule Sync (Disabled per user request)
    # scheduler.add_job(sync_job, IntervalTrigger(minutes=30))
    
    scheduler.start()
    logging.info("Scheduler started.")
