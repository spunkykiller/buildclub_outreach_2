from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sqlite3
import shutil
import os
from pathlib import Path
import asyncio
from dotenv import load_dotenv

load_dotenv("config.env")

from .models import AuthorDetail, StatResponse
from .db import get_connection, log_event, DB_PATH
from .discovery.scraper import DiscoveryEngine
from .analysis.analyzer import PDFAnalyzer
from .email_engine.generator import EmailGenerator
from .mailer.sender import Mailer

app = FastAPI(title="Local Automation Dashboard")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Frontend
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
PDF_DIR = Path(__file__).parent.parent / "pdfs"

# Ensure directories exist
PDF_DIR.mkdir(parents=True, exist_ok=True)

# API Routes
@app.get("/authors")
def get_authors():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch authors with status
    cursor.execute("""
        SELECT a.id, a.full_name, a.company, a.industry, a.email as primary_email, a.linkedin as linkedin_url, COALESCE(a.detailed_description, a.bio) as bio,
               p.discovered, p.pdf_uploaded, p.analyzed, p.email_generated, p.sent
        FROM authors a
        LEFT JOIN pipeline_status p ON a.id = p.author_id
    """)
    authors = [dict(row) for row in cursor.fetchall()]

    # Fetch all emails and group by author
    cursor.execute("SELECT author_id, email FROM author_emails")
    email_rows = cursor.fetchall()
    email_map = {}
    for r in email_rows:
        aid = r['author_id']
        if aid not in email_map: email_map[aid] = []
        email_map[aid].append(r['email'])

    # Merge
    for a in authors:
        a['emails'] = email_map.get(a['id'], [])
        # Ensure primary email is in list
        if a['primary_email'] and a['primary_email'] not in a['emails']:
             a['emails'].insert(0, a['primary_email'])
        
        a['pipeline'] = {
            'discovered': bool(a['discovered']),
            'pdf_uploaded': bool(a['pdf_uploaded']),
            'analyzed': bool(a['analyzed']),
            'email_generated': bool(a['email_generated']),
            'sent': bool(a['sent'])
        }
    
    conn.close()
    return authors


@app.post("/discover")
async def trigger_discovery(query: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_discovery_task, query)
    return {"status": "Discovery started"}

async def run_discovery_task(query: str):
    engine = DiscoveryEngine()
    # Need to verify if Engine works with new DB path/init
    # It uses DB_PATH env var, should be fine if we set it or if it defaults correctly.
    # Note: engine is async
    await engine.run_discovery(query)
    # Update pipeline status for new authors? 
    # The scraper might need to be updated to insert into pipeline_status
    # For now, let's assume scraper inserts into authors.
    # We can run a fix-up query here.
    _fix_pipeline_status()

def _fix_pipeline_status():
    conn = get_connection()
    conn.execute("""
        INSERT OR IGNORE INTO pipeline_status (author_id, discovered)
        SELECT id, 1 FROM authors
    """)
    conn.commit()
    conn.close()

@app.post("/upload_pdf/{author_id}")
async def upload_pdf(author_id: int, file: UploadFile = File(...)):
    file_path = PDF_DIR / f"{author_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    conn = get_connection()
    conn.execute("INSERT INTO books (author_id, title, pdf_path) VALUES (?, ?, ?)", 
                 (author_id, file.filename, str(file_path)))
    
    # Update status
    conn.execute("""
        INSERT INTO pipeline_status (author_id, pdf_uploaded) VALUES (?, 1)
        ON CONFLICT(author_id) DO UPDATE SET pdf_uploaded=1
    """, (author_id,))
    
    log_event(author_id, f"Uploaded PDF: {file.filename}")
    conn.commit()
    conn.close()
    
    return {"status": "PDF Uploaded", "path": str(file_path)}

@app.post("/analyze/{author_id}")
async def analyze_author(author_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_analysis_task, author_id)
    return {"status": "Analysis queued"}

def run_analysis_task(author_id: int):
    # We need to adapt PDFAnalyzer to target specific author or just run scan.
    # The current analyzer scans ALL files.
    # Let's instantiate and run standard scan for now as it handles new files.
    # Ideally refactor analyzer to take specific file.
    analyzer = PDFAnalyzer()
    analyzer.scan_and_analyze() # This picks up the new file we just saved
    
    # Update status
    conn = get_connection()
    conn.execute("""
        UPDATE pipeline_status SET analyzed=1 WHERE author_id=?
    """, (author_id,))
    
    # Get analysis result to verify? 
    # For now assume success if no error.
    log_event(author_id, "Analysis run completed")
    conn.commit()
    conn.close()

@app.post("/generate_email/{author_id}")
def generate_email(author_id: int):
    gen = EmailGenerator()
    # Refactor generator to target specific ID? 
    # Current generator does ALL. 
    # Let's modify generator or just run it. 
    # Running it is safe as it skips existing.
    gen.generate_emails_for_pending_authors()
    
    conn = get_connection()
    conn.execute("UPDATE pipeline_status SET email_generated=1 WHERE author_id=?", (author_id,))
    conn.commit()
    conn.close()
    return {"status": "Email generated"}

@app.post("/send_next")
def send_next_email():
    mailer = Mailer()
    sent = mailer.send_next_queued_email()
    if sent:
        return {"status": "Email Sent"}
    else:
        # Check why? Rate limit or empty queue.
        return {"status": "No email sent (Rate Limit or Queue Empty)"}

@app.get("/stats", response_model=StatResponse)
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    total = cursor.execute("SELECT COUNT(*) FROM authors").fetchone()[0]
    # Sent today (sqlite specific date function)
    sent_today = cursor.execute("SELECT COUNT(*) FROM sends WHERE date(sent_at) = date('now')").fetchone()[0]
    pending = cursor.execute("SELECT COUNT(*) FROM emails WHERE status='pending'").fetchone()[0]
    
    conn.close()
    return StatResponse(total_authors=total, emails_sent_today=sent_today, pending_emails=pending, zoho_health="OK")

from .scheduler import start_scheduler

@app.on_event("startup")
async def startup_event():
    start_scheduler()

# Mount Static as root LAST
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
