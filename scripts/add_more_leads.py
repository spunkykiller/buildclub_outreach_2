import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

leads = [
    {
        "full_name": "Jason Cohen",
        "company": "Smart Bear / WP Engine",
        "book_title": "A Smart Bear (Blog)", # Using blog as context
        "detailed_description": "Founder of WP Engine and Smart Bear. Expert on bootstrapping and scaling SaaS.",
        "context": "your insights on A Smart Bear and building WP Engine",
        "response_probability": 85
    },
    {
        "full_name": "Greg Head",
        "company": "Practical Founders",
        "book_title": "Practical Founders (Blog)",
        "detailed_description": "Founder of Practical Founders. Helps scaling software founders.",
        "context": "your work with Practical Founders",
        "response_probability": 88
    },
    {
        "full_name": "Hiten Shah",
        "company": "Nira",
        "book_title": "Product Habits (Newsletter)",
        "detailed_description": "Co-founder of Crazy Egg, KISSmetrics, Nira. Prolific advisor and investor.",
        "context": "your history building Crazy Egg and KISSmetrics",
        "response_probability": 75
    },
    {
        "full_name": "Noah Kagan",
        "company": "AppSumo",
        "book_title": "Million Dollar Weekend",
        "detailed_description": "Founder of AppSumo. Focused on marketing and launching.",
        "context": "your launch strategies in Million Dollar Weekend",
        "response_probability": 85
    },
    {
        "full_name": "Akin Alabi",
        "company": "NairaBET",
        "book_title": "Small Business Big Money",
        "detailed_description": "Founder of NairaBET. Entrepreneur and politician.",
        "context": "business lessons in Small Business Big Money",
        "response_probability": 80
    },
    {
        "full_name": "Clifford Oravec",
        "company": "Tamboo",
        "book_title": "The Epic Guide to Bootstrapping",
        "detailed_description": "Indie hacker. Writer of The Epic Guide to Bootstrapping.",
        "context": "your Epic Guide to Bootstrapping",
        "response_probability": 90
    },
    {
        "full_name": "Andrew Gazdecki",
        "company": "Acquire.com",
        "book_title": "Getting Acquired",
        "detailed_description": "Founder of Acquire.com. Expert on selling startups.",
        "context": "your insights on exit strategies in Getting Acquired",
        "response_probability": 80
    },
    {
        "full_name": "Dane Maxwell",
        "company": "The Foundation",
        "book_title": "Start From Zero",
        "detailed_description": "Founder of The Foundation. Teaches starting businesses from scratch.",
        "context": "your framework in Start From Zero",
        "response_probability": 85
    },
    {
        "full_name": "Takuya Matsuyama",
        "company": "Inkdrop",
        "book_title": "Inkdrop Journey (Blog)",
        "detailed_description": "Solo dev of Inkdrop. Shares journey on YouTube/Blog.",
        "context": "your journey building Inkdrop as a solo dev",
        "response_probability": 92
    },
    {
        "full_name": "Alexander Isora",
        "company": "Unicorn Platform",
        "book_title": "Unicorn Platform Journey",
        "detailed_description": "Founder of Unicorn Platform. Open startup advocate.",
        "context": "building Unicorn Platform in public",
        "response_probability": 90
    },
    {
        "full_name": "Ryan Law",
        "company": "Ahrefs",
        "book_title": "None",
        "detailed_description": "Director of Content at Ahrefs. Content strategy expert.",
        "context": "your content strategy work at Ahrefs",
        "response_probability": 88
    },
    {
        "full_name": "Joel York",
        "company": "Chaotic Flow",
        "book_title": "Chaotic Flow (Blog)",
        "detailed_description": "SaaS veteran. Writes Chaotic Flow blog.",
        "context": "your SaaS metrics analysis on Chaotic Flow",
        "response_probability": 85
    },
    {
        "full_name": "Sarah Hatter",
        "company": "CoSupport",
        "book_title": "The Customer Support Handbook",
        "detailed_description": "Founder of CoSupport. Expert on customer service.",
        "context": "your philosophy in The Customer Support Handbook",
        "response_probability": 90
    },
    {
        "full_name": "Wade Foster",
        "company": "Zapier",
        "book_title": "None",
        "detailed_description": "Co-founder of Zapier. Remote work pioneer.",
        "context": "scaling Zapier remotely",
        "response_probability": 65
    },
    {
        "full_name": "Mike McDerment",
        "company": "FreshBooks",
        "book_title": "Breaking the Time Barrier",
        "detailed_description": "Co-founder of FreshBooks. Advocates for value-based pricing.",
        "context": "your views on value based pricing in Breaking the Time Barrier",
        "response_probability": 80
    },
    {
        "full_name": "Jeromy Wilson",
        "company": "Niche Academy",
        "book_title": "None",
        "detailed_description": "Founder of Niche Academy. Bootstrapped success.",
        "context": "bootstrapping Niche Academy",
        "response_probability": 90
    },
    {
        "full_name": "Scott Hanselman",
        "company": "Microsoft",
        "book_title": "Hanselminutes",
        "detailed_description": "Programmer, blogger, speaker. Not a typical founder but huge influence.",
        "context": "your work on Hanselminutes and dev culture",
        "response_probability": 80
    },
    {
        "full_name": "Patrick McKenzie",
        "company": "Stripe",
        "book_title": "Kalzumeus (Blog)",
        "detailed_description": "Patio11. Legend in checking engineering/marketing overlap.",
        "context": "your writings on Kalzumeus",
        "response_probability": 75
    },
    {
        "full_name": "Laura Roeder",
        "company": "Paperbell",
        "book_title": "None",
        "detailed_description": "Founder of MeetEdgar and Paperbell. Social media expert.",
        "context": "building MeetEdgar and Paperbell",
        "response_probability": 85
    },
    {
        "full_name": "Randall Kanna",
        "company": "Author",
        "book_title": "The Standout Developer",
        "detailed_description": "Software engineer and author.",
        "context": "your advice in The Standout Developer",
        "response_probability": 88
    },
    {
        "full_name": "Shawn Wang",
        "company": "Swyx",
        "book_title": "The Coding Career Handbook",
        "detailed_description": "Swyx. Developer advocate and founder.",
        "context": "learning in public and The Coding Career Handbook",
        "response_probability": 90
    },
    {
        "full_name": "Daniel Vassallo",
        "company": "Small Bets",
        "book_title": "The Good Parts of AWS",
        "detailed_description": "Former Amazonian. Founder of Small Bets community.",
        "context": "your Small Bets philosophy",
        "response_probability": 88
    },
    {
        "full_name": "Steph Smith",
        "company": "a16z",
        "book_title": "Doing Content Right",
        "detailed_description": "Writer and podcast host. Doing Content Right author.",
        "context": "your guide Doing Content Right",
        "response_probability": 85
    },
    {
        "full_name": "Jakob Greenfeld",
        "company": "Opportunities",
        "book_title": "None",
        "detailed_description": "Indie hacker. Experimenter.",
        "context": "your experiments and Opportunities newsletter",
        "response_probability": 90
    },
    {
        "full_name": "Bananaman",
        "company": "Potion",
        "book_title": "None",
        "detailed_description": "Notion website builder. Indie hacker.",
        "context": "building Potion for Notion",
        "response_probability": 90
    },
    {
        "full_name": "Tony Dinh",
        "company": "TypingMind",
        "book_title": "None",
        "detailed_description": "Indie hacker. Built TypingMind, Xnapper.",
        "context": "your incredible shipping velocity with TypingMind",
        "response_probability": 88
    },
    {
        "full_name": "Danny Postma",
        "company": "HeadshotPro",
        "book_title": "None",
        "detailed_description": "Indie hacker. AI headshots.",
        "context": "your success with AI products like HeadshotPro",
        "response_probability": 85
    },
    {
        "full_name": "Marc Lou",
        "company": "ShipFast",
        "book_title": "None",
        "detailed_description": "Indie hacker. ShipFast boilerplate.",
        "context": "your ShipFast boilerplate and launch style",
        "response_probability": 88
    },
    {
        "full_name": "Sabin Dima",
        "company": "Waydev",
        "book_title": "None",
        "detailed_description": "Founder of Waydev. Git analytics.",
        "context": "building Waydev",
        "response_probability": 85
    },
    {
        "full_name": "Marie Poulin",
        "company": "Notion Mastery",
        "book_title": "None",
        "detailed_description": "Notion expert. Course creator.",
        "context": "your Notion Mastery business",
        "response_probability": 90
    },
    {
        "full_name": "Khe Hy",
        "company": "RadReads",
        "book_title": "None",
        "detailed_description": "Founder of RadReads. Productivity expert.",
        "context": "your work on RadReads and $10k Work",
        "response_probability": 85
    },
    {
        "full_name": "Anne-Laure Le Cunff",
        "company": "Ness Labs",
        "book_title": "None",
        "detailed_description": "Founder of Ness Labs. Neuroscience and productivity.",
        "context": "building Ness Labs and mindful productivity",
        "response_probability": 88
    },
    {
        "full_name": "Courtland Allen",
        "company": "Indie Hackers",
        "book_title": "None",
        "detailed_description": "Founder of Indie Hackers.",
        "context": "growing the Indie Hackers community",
        "response_probability": 80
    },
    {
        "full_name": "Charly Wc",
        "company": "Indie Hacker",
        "book_title": "None",
        "detailed_description": "Indie Maker.",
        "context": "your indie maker journey",
        "response_probability": 85
    },
    {
        "full_name": "Jon Yongfook",
        "company": "Bannerbear",
        "book_title": "None",
        "detailed_description": "Founder of Bannerbear. Open startup.",
        "context": "your journey to $50k MRR with existing transparency",
        "response_probability": 88
    },
    {
        "full_name": "Andrey Azimov",
        "company": "Sheet2Site",
        "book_title": "None",
        "detailed_description": "Hardcore shipping indie hacker.",
        "context": "your hardcore year of shipping projects",
        "response_probability": 85
    },
    {
        "full_name": "Ajay Yadav",
        "company": "Simplified",
        "book_title": "None",
        "detailed_description": "Founder of Simplified.",
        "context": "building Simplified",
        "response_probability": 80
    },
    {
        "full_name": "Guillermo Rauch",
        "company": "Vercel",
        "book_title": "None",
        "detailed_description": "CEO of Vercel. Creator of Next.js.",
        "context": "the impact of Vercel and Next.js",
        "response_probability": 60
    },
    {
        "full_name": "Lee Robinson",
        "company": "Vercel",
        "book_title": "None",
        "detailed_description": "VP DevRel Vercel.",
        "context": "your DevRel work at Vercel",
        "response_probability": 85
    },
    {
        "full_name": "Caleb Porzio",
        "company": "Alpine.js / Livewire",
        "book_title": "None",
        "detailed_description": "Creator of Alpine.js and Livewire.",
        "context": "your work on the TALL stack and sponsorship model",
        "response_probability": 90
    },
    {
        "full_name": "Adam Wathan",
        "company": "Tailwind Labs",
        "book_title": "Refactoring UI",
        "detailed_description": "Creator of Tailwind CSS. Author of Refactoring UI.",
        "context": "changing the web with Tailwind CSS",
        "response_probability": 80
    },
    {
        "full_name": "Steve Schoger",
        "company": "Tailwind Labs",
        "book_title": "Refactoring UI",
        "detailed_description": "Designer. Co-author of Refactoring UI.",
        "context": "design tips in Refactoring UI",
        "response_probability": 85
    },
    {
        "full_name": "Alex Bass",
        "company": "Efficient App",
        "book_title": "None",
        "detailed_description": "Automation expert.",
        "context": "your work with Efficient App",
        "response_probability": 90
    },
     {
        "full_name": "Ben Tossell",
        "company": "Makerpad",
        "book_title": "None",
        "detailed_description": "Founder of Makerpad. No-code pioneer.",
        "context": "pioneering the no-code movement with Makerpad",
        "response_probability": 85
    }
]

def add_more():
    print(f"Adding {len(leads)} more leads...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for lead in leads:
        cursor.execute("SELECT id FROM authors WHERE full_name = ?", (lead['full_name'],))
        existing = cursor.fetchone()
        
        if not existing:
            try:
                cursor.execute("""
                    INSERT INTO authors (full_name, company, discovery_status, detailed_description, response_probability, context)
                    VALUES (?, ?, 'manual_upload_2', ?, ?, ?)
                """, (
                    lead['full_name'], 
                    lead['company'], 
                    lead['detailed_description'], 
                    lead['response_probability'],
                    lead['context']
                ))
                aid = cursor.lastrowid
                
                # Insert mock Book entry
                book_title = lead.get("book_title")
                if book_title and book_title != "None":
                    cursor.execute("INSERT INTO books (author_id, title) VALUES (?, ?)", (aid, book_title))
                else:
                    # Insert dummy book for compatibility if needed, or better, rely on context alone
                    # The generator now checks for context OR analysis/book
                    pass
                
                # Update status
                cursor.execute("INSERT INTO pipeline_status (author_id, discovered, analyzed) VALUES (?, 1, 1)", (aid,))
                
                count += 1
            except Exception as e:
                print(f"Error adding {lead['full_name']}: {e}")
        else:
            print(f"Skipping {lead['full_name']}, already exists.")
            
    conn.commit()
    conn.close()
    print(f"Successfully added {count} NEW leads.")

if __name__ == "__main__":
    add_more()
