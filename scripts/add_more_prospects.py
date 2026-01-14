import sqlite3

# Connect to database
conn = sqlite3.connect('local_system.db')
cursor = conn.cursor()

# Additional 9 prospects to reach 30
new_prospects = [
    {
        "full_name": "Rob Walling",
        "company": "TinySeed",
        "linkedin": "https://www.linkedin.com/in/robwalling",
        "detailed_description": "Founder of Drip (sold to Leadpages) and TinySeed. Pioneer of bootstrapped SaaS movement.",
        "context": "your journey with bootstrapped SaaS and founding TinySeed"
    },
    {
        "full_name": "Rand Fishkin",
        "company": "SparkToro",
        "linkedin": "https://www.linkedin.com/in/randfishkin",
        "detailed_description": "Founder of Moz and SparkToro. Transparent about the realities of VC-funded startups.",
        "context": "your transparent journey with Moz and insights in Lost and Founder"
    },
    {
        "full_name": "Arvid Kahl",
        "company": "FeedbackPanda",
        "linkedin": "https://www.linkedin.com/in/arvidkahl",
        "detailed_description": "Built and sold FeedbackPanda. Writes extensively about bootstrapping and building in public.",
        "context": "building and selling FeedbackPanda and The Bootstrapped Founder"
    },
    {
        "full_name": "Sahil Lavingia",
        "company": "Gumroad",
        "linkedin": "https://www.linkedin.com/in/sahillavingia",
        "detailed_description": "Founder of Gumroad. Pioneered 'calm company' approach after rejecting traditional VC exit path.",
        "context": "your journey with Gumroad and choosing profitability over unicorn status"
    },
    {
        "full_name": "Pieter Levels",
        "company": "Nomad List",
        "linkedin": "https://www.linkedin.com/in/pieterhlevels",
        "detailed_description": "Indie maker who built 40+ startups including Nomad List and RemoteOK. Ships incredibly fast.",
        "context": "your approach to rapid shipping and building 40+ products as a solo founder"
    },
    {
        "full_name": "Hiten Shah",
        "company": "FYI",
        "linkedin": "https://www.linkedin.com/in/hnshah",
        "detailed_description": "Co-founder of Crazy Egg, KISSmetrics, and FYI. Advisor to numerous startups on product and growth.",
        "context": "your experience across multiple startups and product-led growth insights"
    },
    {
        "full_name": "Patrick McKenzie",
        "company": "Stripe",
        "linkedin": "https://www.linkedin.com/in/pmckenzie",
        "detailed_description": "Built Bingo Card Creator, Appointment Reminder. Now works at Stripe. Legendary for writing about business.",
        "context": "your journey from solo bootstrapping to Stripe and your exceptional writing"
    },
    {
        "full_name": "Amy Hoy",
        "company": "Stacking the Bricks",
        "linkedin": "https://www.linkedin.com/in/amyhoy",
        "detailed_description": "Creator of 30x500 course. Bootstrapped multiple products. Expert on teaching founders to sell.",
        "context": "your approach to bootstrapping and teaching founders through 30x500"
    },
    {
        "full_name": "Nathan Barry",
        "company": "ConvertKit",
        "linkedin": "https://www.linkedin.com/in/nathanbarry",
        "detailed_description": "Built ConvertKit from $0 to $30M ARR. Advocate for creators and direct relationship with audience.",
        "context": "building ConvertKit and your philosophy on serving creators"
    }
]

# Insert each prospect
for prospect in new_prospects:
    try:
        cursor.execute("""
            INSERT INTO authors (full_name, company, linkedin, detailed_description, context)
            VALUES (?, ?, ?, ?, ?)
        """, (
            prospect["full_name"],
            prospect["company"],
            prospect["linkedin"],
            prospect["detailed_description"],
            prospect["context"]
        ))
        print(f"+ Added: {prospect['full_name']}")
    except sqlite3.IntegrityError as e:
        print(f"- Skipped {prospect['full_name']}: {e}")

# Initialize pipeline status for new authors
cursor.execute("""
    INSERT OR IGNORE INTO pipeline_status (author_id, discovered)
    SELECT id, 1 FROM authors
""")

conn.commit()

# Verify count
cursor.execute("SELECT COUNT(*) FROM authors")
total = cursor.fetchone()[0]
print(f"\n+ Total prospects in database: {total}")

conn.close()
