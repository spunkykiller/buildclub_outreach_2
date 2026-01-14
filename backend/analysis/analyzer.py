import os
import fitz  # PyMuPDF
import sqlite3
import requests
import json
import logging
from pathlib import Path
from backend.db import get_connection, DB_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assume PDF_DIR is properly set by caller or env, or default relative
PDF_DIR = os.getenv("PDF_DIRECTORY", "pdfs")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_API_URL = "http://localhost:11434/api/generate"

class PDFAnalyzer:
    def __init__(self):
        self.pdf_dir = Path(PDF_DIR)

    def scan_and_analyze(self):
        # Resolve PDF dir relative to root if needed
        if not self.pdf_dir.is_absolute():
            # Assuming running from root
            self.pdf_dir = Path.cwd() / self.pdf_dir
            
        if not self.pdf_dir.exists():
            logging.warning(f"PDF directory {self.pdf_dir} does not exist.")
            return

        for pdf_file in self.pdf_dir.glob("*.pdf"):
            self._process_pdf(pdf_file)

    def _process_pdf(self, pdf_path):
        filename = pdf_path.name
        logging.info(f"Processing {filename}...")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if already processed
        cursor.execute("SELECT id, author_id FROM books WHERE pdf_path LIKE ?", (f"%{filename}",))
        row = cursor.fetchone()
        
        author_id = None
        
        if row:
            logging.info(f"Book entry exists for {filename}.")
            author_id = row['author_id']
            # Check pipeline status
            cursor.execute("SELECT analyzed FROM pipeline_status WHERE author_id=?", (author_id,))
            status = cursor.fetchone()
            if status and status['analyzed']:
                logging.info(f"Already analyzed {filename}.")
                conn.close()
                return
        else:
            # Create new entry if it appeared in folder but not in API upload flow
            # (Fallback logic)
            pass

        if not author_id:
             # Basic fallback logic if not uploaded via API
             # ... (Skipped for brevity, assuming API upload flow prefers)
             conn.close()
             return

        # Extract Text
        text = self._extract_text(pdf_path)
        if not text:
            logging.warning(f"No text extracted from {filename}")
            conn.close()
            return
        
        # Analyze
        analysis_result = self._analyze_text_with_ollama(text)
        
        # Save Analysis
        if analysis_result:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO analysis 
                    (author_id, philosophy, principles, tone, beliefs, opportunities)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    author_id,
                    analysis_result.get('philosophy', ''),
                    analysis_result.get('principles', ''),
                    analysis_result.get('tone', ''),
                    analysis_result.get('beliefs', ''),
                    analysis_result.get('opportunities', '')
                ))
                
                # Update pipeline
                cursor.execute("""
                    INSERT INTO pipeline_status (author_id, analyzed) VALUES (?, 1)
                    ON CONFLICT(author_id) DO UPDATE SET analyzed=1
                """, (author_id,))
                
                conn.commit()
                logging.info(f"Analysis saved for {filename}")
            except Exception as e:
                logging.error(f"Error saving analysis: {e}")
        
        conn.close()

    def _extract_text(self, pdf_path, max_pages=20):
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for i, page in enumerate(doc):
                if i >= max_pages:
                    break
                text += page.get_text()
            return text
        except Exception as e:
            logging.error(f"Error reading PDF {pdf_path}: {e}")
            return None

    def _analyze_text_with_ollama(self, text):
        prompt = f"""
        You are an expert literary and business analyst. Analyze the following book excerpt.
        Extract the following information in JSON format:
        - philosophy: The core business or life philosophy.
        - principles: List of 3 key principles.
        - tone: The writing tone (e.g., authoritative, friendly, humble).
        - beliefs: Key beliefs about the world or industry.
        - opportunities: Potential angles for collaboration.

        Text Excerpt:
        {text[:4000]} 
        
        Respond ONLY with valid JSON.
        """
        
        try:
            response = requests.post(OLLAMA_API_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            })
            response.raise_for_status()
            data = response.json()
            return json.loads(data['response'])
        except Exception as e:
            logging.error(f"Ollama analysis failed: {e}")
            return None
