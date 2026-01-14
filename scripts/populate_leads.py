import sqlite3
import os
import sys

# Add parent directory to path to allow imports if needed, though we use direct sqlite here
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

leads = [
    # Niche / Bootstrapped / Indie
    {
        "full_name": "Arvid Kahl",
        "company": "FeedbackPanda",
        "book_title": "Zero to Sold",
        "detailed_description": "Co-founder of FeedbackPanda, a SaaS for online teachers. Bootstrapped to $55k MRR and sold. Writes about building audience-first businesses.",
        "context": "your journey bootstrapping FeedbackPanda and your insights in Zero to Sold",
        "response_probability": 90
    },
    {
        "full_name": "Rob Walling",
        "company": "TinySeed",
        "book_title": "The SaaS Playbook",
        "detailed_description": "Serial entrepreneur and investor. Founder of Drip (sold). Host of Startups for the Rest of Us. Focuses on B2B SaaS.",
        "context": "your work with TinySeed and the practical wisdom in The SaaS Playbook",
        "response_probability": 85
    },
    {
        "full_name": "Rand Fishkin",
        "company": "SparkToro",
        "book_title": "Lost and Founder",
        "detailed_description": "Founder of Moz and SparkToro. Known for transparency about the struggles of startup life and challenging VC norms.",
        "context": "your transparency in Lost and Founder and your current work with SparkToro",
        "response_probability": 85
    },
    {
        "full_name": "Sahil Lavingia",
        "company": "Gumroad",
        "book_title": "The Minimalist Entrepreneur",
        "detailed_description": "Founder of Gumroad. Advocate for sustainable, profitable businesses over growth-at-all-costs.",
        "context": "your philosophy in The Minimalist Entrepreneur and journey with Gumroad",
        "response_probability": 88
    },
    {
        "full_name": "Jason Fried",
        "company": "37signals",
        "book_title": "Rework",
        "detailed_description": "Co-founder of Basecamp/37signals. Proponent of calm companies and remote work.",
        "context": "your philosophy on calm companies and Rework",
        "response_probability": 80
    },
    {
        "full_name": "David Heinemeier Hansson",
        "company": "37signals",
        "book_title": "Remote",
        "detailed_description": "Co-founder of Basecamp. Creator of Ruby on Rails. Outspoken critic of big tech monopolies.",
        "context": "your views on remote work and building sustainable software businesses",
        "response_probability": 80
    },
    {
        "full_name": "Paul Jarvis",
        "company": "Fathom Analytics",
        "book_title": "Company of One",
        "detailed_description": "Designer and writer. Co-founder of Fathom Analytics. Advocates for staying small and profitable.",
        "context": "the concept of Company of One and staying small by choice",
        "response_probability": 85
    },
    {
        "full_name": "Ash Maurya",
        "company": "LEANSTACK",
        "book_title": "Running Lean",
        "detailed_description": "Creator of the Lean Canvas. Focuses on systematic scaling and problem/solution fit.",
        "context": "your work on the Lean Canvas and Running Lean",
        "response_probability": 85
    },
    {
        "full_name": "Nir Eyal",
        "company": "NirAndFar",
        "book_title": "Hooked",
        "detailed_description": "Author and lecturer. Expert on habit-forming technology and distraction.",
        "context": "your research in Hooked and Indistractable",
        "response_probability": 82
    },
    {
        "full_name": "Marty Neumeier",
        "company": "Liquid Agency",
        "book_title": "The Brand Gap",
        "detailed_description": "Brand expert. Focuses on the gap between business strategy and design.",
        "context": "your insights on branding in The Brand Gap",
        "response_probability": 80
    },
    {
        "full_name": "Lou Downe",
        "company": "School of Good Services",
        "book_title": "Good Services",
        "detailed_description": "Service design expert. Former Design Director of the UK Government.",
        "context": "your principles of service design in Good Services",
        "response_probability": 85
    },
    {
        "full_name": "April Dunford",
        "company": "Ambient Strategy",
        "book_title": "Obviously Awesome",
        "detailed_description": "Positioning expert. Helps B2B tech companies position their products.",
        "context": "your framework for positioning in Obviously Awesome",
        "response_probability": 90
    },
    {
        "full_name": "Michele Hansen",
        "company": "Geocodio",
        "book_title": "Deploy Empathy",
        "detailed_description": "Co-founder of Geocodio. Expert on customer research and empathy in business.",
        "context": "your approach to customer research in Deploy Empathy",
        "response_probability": 92
    },
    {
        "full_name": "Pieter Levels",
        "company": "Nomad List",
        "book_title": "MAKE",
        "detailed_description": "Indie hacker. Founder of Nomad List and Remote OK. Known for shipping projects fast.",
        "context": "your journey shipping startups and the MAKE book",
        "response_probability": 85
    },
    {
        "full_name": "Adii Pienaar",
        "company": "Cogsy",
        "book_title": "Life Profitability",
        "detailed_description": "Founder of WooCommerce (sold) and Cogsy. Writes about work-life balance and profitability.",
        "context": "your perspective on life profitability and building sustainable ventures",
        "response_probability": 88
    },
    {
        "full_name": "Gabriel Weinberg",
        "company": "DuckDuckGo",
        "book_title": "Traction",
        "detailed_description": "CEO of DuckDuckGo. Co-author of Traction, a framework for startup growth.",
        "context": "the Traction framework and building privacy-focused tech",
        "response_probability": 75
    },
    {
        "full_name": "Justin Mares",
        "company": "Kettle & Fire",
        "book_title": "Traction",
        "detailed_description": "Co-author of Traction. Founder of Kettle & Fire and Perfect Keto.",
        "context": "your insights in Traction and experience in D2C",
        "response_probability": 80
    },
    {
        "full_name": "Eric Ries",
        "company": "Long-Term Stock Exchange",
        "book_title": "The Lean Startup",
        "detailed_description": "Author of The Lean Startup. CEO of Long-Term Stock Exchange. Revolutionized startup methodology.",
        "context": "the impact of The Lean Startup and your new work with LTSE",
        "response_probability": 60
    },
    {
        "full_name": "Ben Horowitz",
        "company": "Andreessen Horowitz",
        "book_title": "The Hard Thing About Hard Things",
        "detailed_description": "Co-founder of a16z. Former CEO of Opsware. Writes about the psychological toll of leadership.",
        "context": "the lessons in The Hard Thing About Hard Things",
        "response_probability": 50
    },
    {
        "full_name": "Jessica Livingston",
        "company": "Y Combinator",
        "book_title": "Founders at Work",
        "detailed_description": "Co-founder of Y Combinator. Interviewed hundreds of founders.",
        "context": "your interviews in Founders at Work and role at YC",
        "response_probability": 60
    },
    {
        "full_name": "Chris Guillebeau",
        "company": "The Art of Non-Conformity",
        "book_title": "The $100 Startup",
        "detailed_description": "Author and traveler. Focuses on micro-businesses and freedom.",
        "context": "the stories in The $100 Startup",
        "response_probability": 85
    },
    {
        "full_name": "MJ DeMarco",
        "company": "The Fastlane Forum",
        "book_title": "The Millionaire Fastlane",
        "detailed_description": "Founder of Limos.com (sold). Writes about wealth creation and entrepreneurship.",
        "context": "your unvarnished truth in The Millionaire Fastlane",
        "response_probability": 80
    },
    {
        "full_name": "Dan Norris",
        "company": "WP Curve",
        "book_title": "The 7 Day Startup",
        "detailed_description": "Founder of WP Curve (sold to GoDaddy). Advocate for launching quickly.",
        "context": "the methodology in The 7 Day Startup",
        "response_probability": 85
    },
    {
        "full_name": "Allan Dib",
        "company": "Successwise",
        "book_title": "The 1-Page Marketing Plan",
        "detailed_description": "Serial entrepreneur and marketer. Simplifies marketing for small businesses.",
        "context": "the simplicity of The 1-Page Marketing Plan",
        "response_probability": 85
    },
    {
        "full_name": "Alex Hormozi",
        "company": "Acquisition.com",
        "book_title": "$100M Offers",
        "detailed_description": "Founder of GymLaunch. Expert on offers and scaling service businesses.",
        "context": "your framework for creating offers in $100M Offers",
        "response_probability": 70
    },
    {
        "full_name": "Nathan Barry",
        "company": "ConvertKit",
        "book_title": "Authority",
        "detailed_description": "Founder of ConvertKit. Writes about building audiences and SaaS.",
        "context": "your journey building ConvertKit and the lessons in Authority",
        "response_probability": 85
    },
    {
        "full_name": "DHH",
        "company": "37signals",
        "book_title": "It Doesn't Have to Be Crazy at Work",
        "detailed_description": "Creator of Rails. Co-founder Basecamp. Anti-hustle culture advocate.",
        "context": "your views on calm profitable companies",
        "response_probability": 80
    },
    {
        "full_name": "Tony Fadell",
        "company": "Build Collective",
        "book_title": "Build",
        "detailed_description": "Creator of iPod, Nest. Writes about product design and management.",
        "context": "your product wisdom in Build",
        "response_probability": 55
    },
    {
        "full_name": "Tiago Forte",
        "company": "Forte Labs",
        "book_title": "Building a Second Brain",
        "detailed_description": "Productivity expert. Founder of Forte Labs.",
        "context": "the concepts in Building a Second Brain",
        "response_probability": 80
    },
    {
        "full_name": "James Clear",
        "company": "JamesClear.com",
        "book_title": "Atomic Habits",
        "detailed_description": "Writer and entrepreneur. Expert on habit formation.",
        "context": "the systems approach in Atomic Habits",
        "response_probability": 50
    },
    {
        "full_name": "Josh Kaufman",
        "company": "Personal MBA",
        "book_title": "The Personal MBA",
        "detailed_description": "Independent business educator. Synthesizes business concepts.",
        "context": "the comprehensive overview in The Personal MBA",
        "response_probability": 82
    },
    {
        "full_name": "Ramit Sethi",
        "company": "I Will Teach You To Be Rich",
        "book_title": "I Will Teach You To Be Rich",
        "detailed_description": "Founder of IWT. Focuses on personal finance and psychology.",
        "context": "your psychology-first approach to business",
        "response_probability": 65
    },
    {
        "full_name": "Noah Kagan",
        "company": "AppSumo",
        "book_title": "Million Dollar Weekend",
        "detailed_description": "Founder of AppSumo. Early FB/Mint employee. Focuses on marketing and launching.",
        "context": "your energy and tactics in Million Dollar Weekend",
        "response_probability": 85
    },
    {
        "full_name": "Ali Abdaal",
        "company": "Ali Abdaal Ltd",
        "book_title": "Feel-Good Productivity",
        "detailed_description": "YouTuber and entrepreneur. Writes about productivity and creator economy.",
        "context": "your approach to feel-good productivity",
        "response_probability": 80
    },
    {
        "full_name": "Pat Flynn",
        "company": "Smart Passive Income",
        "book_title": "Superfans",
        "detailed_description": "Podcaster and entrepreneur. Expert on affiliate marketing and community.",
        "context": "your ideas on building Superfans",
        "response_probability": 85
    },
    {
        "full_name": "John Warrillow",
        "company": "The Value Builder System",
        "book_title": "Built to Sell",
        "detailed_description": "Founder of The Value Builder System. Expert on company exit value.",
        "context": "the framework in Built to Sell",
        "response_probability": 82
    },
    {
        "full_name": "Mike Michalowicz",
        "company": "Profit First Professionals",
        "book_title": "Profit First",
        "detailed_description": "Author and entrepreneur. reinvented accounting for small biz.",
        "context": "the philosophy of Profit First",
        "response_probability": 85
    },
     {
        "full_name": "Gino Wickman",
        "company": "EOS Worldwide",
        "book_title": "Traction (EOS)",
        "detailed_description": "Creator of EOS (Entrepreneurial Operating System).",
        "context": "the impact of EOS on small businesses",
        "response_probability": 75
    },
    {
        "full_name": "Verne Harnish",
        "company": "Gazelles",
        "book_title": "Scaling Up",
        "detailed_description": "Founder of EO (Entrepreneurs' Organization). Expert on scaling.",
        "context": "the Scaling Up framework",
        "response_probability": 70
    },
    {
        "full_name": "Elad Gil",
        "company": "Color Genomics",
        "book_title": "High Growth Handbook",
        "detailed_description": "Investor and advisor. Former VP at Twitter. Expert on scaling startups.",
        "context": "the tactical advice in High Growth Handbook",
        "response_probability": 65
    },
    {
        "full_name": "Scott Belsky",
        "company": "Behance",
        "book_title": "The Messy Middle",
        "detailed_description": "Founder of Behance. CPO at Adobe. Writes about the endurance required for startups.",
        "context": "navigating The Messy Middle of projects",
        "response_probability": 70
    },
    {
        "full_name": "Julie Zhuo",
        "company": "Sundial",
        "book_title": "The Making of a Manager",
        "detailed_description": "Former VP Design at FB. Co-founder of Sundial. Writes about management.",
        "context": "your insights in The Making of a Manager",
        "response_probability": 75
    },
    {
        "full_name": "Lenny Rachitsky",
        "company": "Lenny's Newsletter",
        "book_title": "The Racecar Framework (Blog/Guide)", # Not a book per se but very influential
        "detailed_description": "Former Product Lead at Airbnb. Writer of top tech newsletter.",
        "context": "your insights on product growth and community",
        "response_probability": 85
    },
    {
        "full_name": "Gagan Biyani",
        "company": "Maven",
        "book_title": "None", # Notable founder, context could be Podcast/Article
        "detailed_description": "Co-founder of Udemy and Maven. Reviewing cohort based courses.",
        "context": "your work building Udemy and Maven",
        "response_probability": 85
    },
    {
        "full_name": "Andrew Chen",
        "company": "a16z",
        "book_title": "The Cold Start Problem",
        "detailed_description": "Partner at a16z. Former Uber growth. Expert on network effects.",
        "context": "network effects and The Cold Start Problem",
        "response_probability": 65
    },
    {
        "full_name": "Ryan Hoover",
        "company": "Product Hunt",
        "book_title": "Hooked (Contributed)",
        "detailed_description": "Founder of Product Hunt. Investor.",
        "context": "building the Product Hunt community",
        "response_probability": 80
    },
    {
        "full_name": "Alexis Ohanian",
        "company": "Seven Seven Six",
        "book_title": "Without Their Permission",
        "detailed_description": "Co-founder of Reddit. Investor.",
        "context": "your story in Without Their Permission",
        "response_probability": 60
    },
    {
        "full_name": "Peter Thiel",
        "company": "Founders Fund",
        "book_title": "Zero to One",
        "detailed_description": "PayPal Mafia. First investor in FB.",
        "context": "the contrarian views in Zero to One",
        "response_probability": 40
    },
    {
        "full_name": "Walter Isaacson",
        "company": "Author",
        "book_title": "Steve Jobs",
        "detailed_description": "Biographer of Jobs, Musk. Not a founder but expert on them.",
        "context": "your study of great founders like Jobs and Musk",
        "response_probability": 50
    },
    {
        "full_name": "Brad Feld",
        "company": "Techstars",
        "book_title": "Venture Deals",
        "detailed_description": "Co-founder Techstars. Investor.",
        "context": "demystifying VC in Venture Deals",
        "response_probability": 75
    },
    {
        "full_name": "Derek Sivers",
        "company": "CD Baby",
        "book_title": "Anything You Want",
        "detailed_description": "Founder of CD Baby. Philosopher of entrepreneurship.",
        "context": "your philosophy in Anything You Want",
        "response_probability": 88
    },
    {
        "full_name": "Kander & Yang",
        "company": "Clearbit",
        "book_title": "The Data Driven Sales", 
        "detailed_description": "Founders of Clearbit.",
        "context": "your approach to data driven growth",
        "response_probability": 80
    }
]

def populate():
    print(f"Populating {len(leads)} leads...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for lead in leads:
        # Check if exists
        cursor.execute("SELECT id FROM authors WHERE full_name = ?", (lead['full_name'],))
        existing = cursor.fetchone()
        
        if not existing:
            try:
                cursor.execute("""
                    INSERT INTO authors (full_name, company, discovery_status, detailed_description, response_probability, context)
                    VALUES (?, ?, 'manual_upload', ?, ?, ?)
                """, (
                    lead['full_name'], 
                    lead['company'], 
                    lead['detailed_description'], 
                    lead['response_probability'],
                    lead['context']
                ))
                aid = cursor.lastrowid
                
                # Insert mock Book entry so generator picks it up
                book_title = lead.get("book_title")
                if book_title and book_title != "None":
                    cursor.execute("INSERT INTO books (author_id, title) VALUES (?, ?)", (aid, book_title))
                
                # Update status
                cursor.execute("INSERT INTO pipeline_status (author_id, discovered, analyzed) VALUES (?, 1, 1)", (aid,))
                
                count += 1
            except Exception as e:
                print(f"Error adding {lead['full_name']}: {e}")
        else:
            print(f"Skipping {lead['full_name']}, already exists.")
            
    conn.commit()
    conn.close()
    print(f"Successfully added {count} new leads.")

if __name__ == "__main__":
    populate()
