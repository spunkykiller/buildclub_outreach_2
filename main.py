import argparse
import asyncio
from discovery.scraper import DiscoveryEngine
from analysis.analyzer import PDFAnalyzer
from email_engine.generator import EmailGenerator
from mailer.sender import Mailer
from sheets.syncer import SheetSyncer
import db.database as db

def init_system():
    print("Initializing Database...")
    db.init_db()

def run_discovery(query):
    print(f"Running discovery for '{query}'...")
    engine = DiscoveryEngine()
    asyncio.run(engine.run_discovery(query))

def run_analysis():
    print("Running PDF Analysis...")
    analyzer = PDFAnalyzer()
    analyzer.scan_and_analyze()

def run_generator():
    print("Running Email Generator...")
    gen = EmailGenerator()
    gen.generate_emails_for_pending_authors()

def run_mailer():
    print("Attempting to send ONE email...")
    mailer = Mailer()
    sent = mailer.send_next_queued_email()
    if not sent:
        print("No email sent (Queue empty or Rate Limit active).")

def run_sync():
    print("Syncing to Google Sheets...")
    syncer = SheetSyncer()
    syncer.sync_db_to_sheet()

def main():
    parser = argparse.ArgumentParser(description="Local Automation System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("init", help="Initialize the database")
    
    disc_parser = subparsers.add_parser("discovery", help="Run Data Discovery")
    disc_parser.add_argument("--query", default="Founder who wrote a book", help="Search query")
    
    subparsers.add_parser("analysis", help="Run PDF Analysis")
    subparsers.add_parser("generate", help="Run Email Generator")
    subparsers.add_parser("send", help="Send *one* email (respects rate limit)")
    subparsers.add_parser("sync", help="Sync to Google Sheets")
    subparsers.add_parser("scheduler", help="Run the Scheduler Daemon")
    
    args = parser.parse_args()

    if args.command == "init":
        init_system()
    elif args.command == "discovery":
        run_discovery(args.query)
    elif args.command == "analysis":
        run_analysis()
    elif args.command == "generate":
        run_generator()
    elif args.command == "send":
        run_mailer()
    elif args.command == "sync":
        run_sync()
    elif args.command == "scheduler":
        import scheduler
        scheduler.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
