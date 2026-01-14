import asyncio
import logging
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import sqlite3
import os
from backend.db import get_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DiscoveryEngine:
    def __init__(self):
        pass

    async def run_discovery(self, query="Founder who wrote a book"):
        logging.info(f"Starting discovery with query: {query}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            search_url = f"https://www.google.com/search?q={query}"
            await page.goto(search_url)
            await page.wait_for_timeout(2000) 
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            results = self._parse_google_results(soup)
            
            for result in results:
                await self._save_lead(result)
                
            await browser.close()
        logging.info("Discovery complete.")

    def _parse_google_results(self, soup):
        results = []
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = anchors[0].find('h3')
                if title:
                    title_text = title.text
                    results.append({
                        'full_name': self._extract_name_from_title(title_text),
                        'source_url': link,
                        'raw_title': title_text
                    })
        return results

    def _extract_name_from_title(self, title):
        parts = title.split(' - ')
        if len(parts) > 0:
            return parts[0].strip()
        return "Unknown"

    async def _save_lead(self, data):
        if not data.get('full_name') or data['full_name'] == "Unknown":
            return

        conn = get_connection()
        try:
            # Insert into authors
            # Also update pipeline_status
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM authors WHERE email = ? OR (email IS NULL AND full_name = ?)", 
                           (None, data['full_name'])) # Weak check
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO authors (full_name, source_url, discovery_status)
                    VALUES (?, ?, 'discovered')
                """, (data['full_name'], data['source_url']))
                new_id = cursor.lastrowid
                
                # Update pipeline
                cursor.execute("INSERT OR IGNORE INTO pipeline_status (author_id, discovered) VALUES (?, 1)", (new_id,))
                conn.commit()
                logging.info(f"Saved potential lead: {data['full_name']}")
            else:
                logging.info(f"Lead {data['full_name']} already exists.")
        except Exception as e:
            logging.error(f"Error saving lead {data['full_name']}: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    import asyncio
    engine = DiscoveryEngine()
    asyncio.run(engine.run_discovery())
