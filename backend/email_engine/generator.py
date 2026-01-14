from .templates import FORMAL_TEMPLATE, FRIENDLY_TEMPLATE, SHORT_TEMPLATE, PODCAST_TEMPLATE
from jinja2 import Template
import sqlite3
import os
from backend.db import get_connection

class EmailGenerator:
    def __init__(self):
        pass

    def generate_emails_for_pending_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get authors who have analysis but no email generated yet
        # Check pipeline_status or emails table
        cursor.execute("""
            SELECT a.id, a.full_name, a.context, b.title as book_title, an.philosophy, an.principles, an.tone, an.opportunities
            FROM authors a
            LEFT JOIN books b ON a.id = b.author_id
            LEFT JOIN analysis an ON a.id = an.author_id
            LEFT JOIN emails e ON a.id = e.author_id
            WHERE e.author_id IS NULL AND (an.author_id IS NOT NULL OR a.context IS NOT NULL)
        """)
        
        rows = cursor.fetchall()
        
        for row in rows:
            self._create_email_entry(dict(row), cursor)
            
        conn.commit()
        conn.close()

    def _create_email_entry(self, data, cursor):
        context = {
            "author_name": data["full_name"],
            "book_title": data["book_title"],
            "philosophy": self._truncate(data["philosophy"], 50),
            "principles": self._truncate(data["principles"], 50),
            "opportunities": self._truncate(data["opportunities"], 50),
            "context": data.get("context")
        }
        
        if data.get("context"):
            podcast_body = Template(PODCAST_TEMPLATE).render(context)
            selected = "podcast"
            cursor.execute("""
                INSERT INTO emails (author_id, subject, body_formal, body_friendly, body_short, selected_variant, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """, (
                data["id"],
                "Invitation to share your founder journey on a podcast", 
                podcast_body, "", "", selected
            ))
        else:
            formal = Template(FORMAL_TEMPLATE).render(context)
            friendly = Template(FRIENDLY_TEMPLATE).render(context)
            short = Template(SHORT_TEMPLATE).render(context)
            
            tone = data["tone"].lower() if data["tone"] else ""
            if "authoritative" in tone or "formal" in tone:
                selected = "formal"
            elif "casual" in tone or "humorous" in tone:
                selected = "friendly"
            else:
                selected = "short"
                
            cursor.execute("""
                INSERT INTO emails (author_id, subject, body_formal, body_friendly, body_short, selected_variant, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """, (
                data["id"],
                f"Regarding {data['book_title']}",
                formal, friendly, short, selected
            ))
        
        # Update Pipeline
        cursor.execute("""
            INSERT INTO pipeline_status (author_id, email_generated) VALUES (?, 1)
            ON CONFLICT(author_id) DO UPDATE SET email_generated=1
        """, (data["id"],))
        
        print(f"Generated email draft for {data['full_name']} (Variant: {selected})")

    def _truncate(self, text, length):
        if not text: return ""
        return text[:length] + "..." if len(text) > length else text
