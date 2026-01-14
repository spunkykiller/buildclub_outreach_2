import sqlite3
import os
from pathlib import Path
from backend.db import get_connection

# List of 50 Entrepreneur Authors
# Note: Emails are placeholders or public guesses where likely (standard patterns).
# Real outreach requires verification.
LEADS = [
    ("Jason Fried", "Basecamp", "It Doesn't Have to Be Crazy at Work", "jason@basecamp.com", "Remote Work, Calm Business"),
    ("David Heinemeier Hansson", "Basecamp", "Rework", "dhh@basecamp.com", "SaaS, Ruby on Rails"),
    ("Pieter Levels", "Nomad List", "Make - The Indie Maker Handbook", "pieter@nomadlist.com", "Indie Hacking, Digital Nomad"),
    ("Arvid Kahl", "FeedbackPanda", "Zero to Sold", "arvid@thebootstrappedfounder.com", "Bootstrapping, SaaS"),
    ("Sahil Lavingia", "Gumroad", "The Minimalist Entrepreneur", "sahil@gumroad.com", "Creator Economy"),
    ("Paul Graham", "Y Combinator", "Hackers & Painters", "pg@ycombinator.com", "Startups, Lisp"),
    ("Peter Thiel", "PayPal/Palantir", "Zero to One", "peter.thiel@foundersfund.com", "Monopoly, Tech"),
    ("Ben Horowitz", "Andreessen Horowitz", "The Hard Thing About Hard Things", "ben@a16z.com", "Management, VC"),
    ("Eric Ries", "IMVU", "The Lean Startup", "eric@theleanstartup.com", "Lean Methodology"),
    ("Rand Fishkin", "SparkToro", "Lost and Founder", "rand@sparktoro.com", "Marketing, SEO"),
    ("Gabriel Weinberg", "DuckDuckGo", "Traction", "gabriel@duckduckgo.com", "Privacy, Growth"),
    ("Nir Eyal", "NirAndFar", "Hooked", "nir@nirandfar.com", "Behavioral Design"),
    ("James Clear", "JamesClear.com", "Atomic Habits", "james@jamesclear.com", "Habits, Productivity"),
    ("Tim Ferriss", "The 4-Hour Workweek", "The 4-Hour Workweek", "tim@fourhourworkweek.com", "Lifestyle Design"),
    ("Seth Godin", "Seth's Blog", "This Is Marketing", "seth@sethgodin.com", "Marketing"),
    ("Gary Vaynerchuk", "VaynerMedia", "Crushing It!", "gary@vaynermedia.com", "Social Media"),
    ("Alex Hormozi", "Acquisition.com", "$100M Offers", "alex@acquisition.com", "Sales, Offers"),
    ("Naval Ravikant", "AngelList", "The Almanack of Naval Ravikant", "naval@angellist.com", "Wealth, Happiness"),
    ("Balaji Srinivasan", "Coinbase (Ex-CTO)", "The Network State", "balaji@balajis.com", "Crypto, Future"),
    ("Tiago Forte", "Forte Labs", "Building a Second Brain", "tiago@fortelabs.co", "PKM, Productivity"),
    ("Ali Abdaal", "Part-Time YouTuber Academy", "Feel-Good Productivity", "ali@aliabdaal.com", "Productivity, YouTube"),
    ("Codie Sanchez", "Contrarian Thinking", "Main Street Millionaire", "codie@contrarianthinking.co", "Investing, Small Biz"),
    ("Nathan Barry", "ConvertKit", "Authority", "nathan@convertkit.com", "Creators, Email"),
    ("Hiten Shah", "Kissmetrics", "The Fernandez & Shah Playbook", "hiten@kissmetrics.com", "SaaS, Product"),
    ("Des Traynor", "Intercom", "Intercom on Product Management", "des@intercom.com", "Product Strategy"),
    ("Dharmesh Shah", "HubSpot", "Inbound Marketing", "dharmesh@hubspot.com", "Inbound, SaaS"),
    ("Brian Chesky", "Airbnb", "Airbnb Story (Subject)", "brian@airbnb.com", "Design, Travel"),
    ("Reid Hoffman", "LinkedIn", "The Alliance", "reid@linkedin.com", "Networking"),
    ("Satya Nadella", "Microsoft", "Hit Refresh", "satya.nadella@microsoft.com", "Leadership"),
    ("Phil Knight", "Nike", "Shoe Dog", "phil.knight@nike.com", "Retail, Brand"),
    ("Ray Dalio", "Bridgewater", "Principles", "ray@bridgewater.com", "Investing, Life"),
    ("Tony Fadell", "Nest", "Build", "tony@nest.com", "Hardware, Design"),
    ("Marc Randolph", "Netflix", "That Will Never Work", "marc@marcrandolph.com", "Streaming, Startups"),
    ("Derek Sivers", "CD Baby", "Anything You Want", "derek@sivers.org", "Indie, Philosophy"),
    ("Austin Kleon", "Writer", "Show Your Work!", "austin@austinkleon.com", "Creativity"),
    ("Adam Grant", "Wharton", "Originals", "adam@adamgrant.net", "Psychology"),
    ("Cal Newport", "Georgetown", "Deep Work", "cal@calnewport.com", "Focus, Digital Minimalism"),
    ("Ryan Holiday", "Daily Stoic", "The Obstacle Is the Way", "ryan@ryanholiday.net", "Stoicism"),
    ("Mark Manson", "Author", "The Subtle Art of Not Giving a F*ck", "mark@markmanson.net", "Self Help"),
    ("Morgan Housel", "Collab Fund", "The Psychology of Money", "morgan@collabfund.com", "Finance"),
    ("Ann Handley", "MarketingProfs", "Everybody Writes", "ann@marketingprofs.com", "Writing, Marketing"),
    ("April Dunford", "Ambient", "Obviously Awesome", "april@aprildunford.com", "zPositioning"),
    ("Lenny Rachitsky", "Lenny's Newsletter", "The Racecar Growth Framework", "lenny@lennysnewsletter.com", "Product, Growth"),
    ("Kieran Flanagan", "Zapier (CMO)", "The Growth Strategy", "kieran@zapier.com", "Marketing"),
    ("Peep Laja", "CXL", "Conversion Optimization", "peep@cxl.com", "CRO"),
    ("Dave Gerhardt", "Exit Five", "Founder Brand", "dave@exitfive.com", "B2B Marketing"),
    ("Chris Voss", "Black Swan Group", "Never Split the Difference", "chris@blackswanltd.com", "Negotiation"),
    ("Jocko Willink", "Echelon Front", "Extreme Ownership", "jocko@echelonfront.com", "Leadership"),
    ("David Goggins", "Self", "Can't Hurt Me", "david@davidgoggins.com", "Resilience"),
    ("Robert Kiyosaki", "Rich Dad", "Rich Dad Poor Dad", "robert@richdad.com", "Finance")
]

def seed_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"Seeding {len(LEADS)} leads...")
    
    count = 0
    for name, company, book, email, industry in LEADS:
        try:
            # 1. Insert Author
            # Check exist
            cursor.execute("SELECT id FROM authors WHERE full_name=?", (name,))
            exist = cursor.fetchone()
            
            if exist:
                author_id = exist[0]
                # Update email if missing
                cursor.execute("UPDATE authors SET email=?, company=?, industry=? WHERE id=?", 
                               (email, company, industry, author_id))
            else:
                cursor.execute("""
                    INSERT INTO authors (full_name, company, industry, email, discovery_status)
                    VALUES (?, ?, ?, ?, 'seeded')
                """, (name, company, industry, email))
                author_id = cursor.lastrowid
                
            # 2. Insert Book
            cursor.execute("SELECT id FROM books WHERE author_id=? AND title=?", (author_id, book))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO books (author_id, title) VALUES (?, ?)", (author_id, book))

            # 3. Pipeline Status
            cursor.execute("""
                INSERT INTO pipeline_status (author_id, discovered) VALUES (?, 1)
                ON CONFLICT(author_id) DO UPDATE SET discovered=1
            """, (author_id,))
            
            count += 1
        except Exception as e:
            print(f"Error inserting {name}: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully seeded {count} leads!")

if __name__ == "__main__":
    seed_db()
