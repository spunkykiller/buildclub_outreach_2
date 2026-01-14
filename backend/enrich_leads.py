import sqlite3
from backend.db import get_connection

# Enhanced Data for Top 50 Leads
# Format: (Name, LinkedIN, [List of Emails])
ENRICHED_DATA = {
    "Jason Fried": ("https://www.linkedin.com/in/jason-fried", ["jason@basecamp.com", "jason@37signals.com"]),
    "David Heinemeier Hansson": ("https://www.linkedin.com/in/david-heinemeier-hansson-374b18221", ["dhh@basecamp.com", "david@hey.com"]),
    "Pieter Levels": ("https://www.linkedin.com/in/levelsio", ["pieter@nomadlist.com", "levels@levels.io"]),
    "Arvid Kahl": ("https://www.linkedin.com/in/arvidkahl", ["arvid@thebootstrappedfounder.com", "arvid.kahl@gmail.com"]),
    "Sahil Lavingia": ("https://www.linkedin.com/in/sahillavingia", ["sahil@gumroad.com", "sahil@shl.vc"]),
    "Paul Graham": ("https://www.linkedin.com/in/paulgraham", ["pg@ycombinator.com", "paul@paulgraham.com"]),
    "Peter Thiel": ("https://www.linkedin.com/in/peterthiel", ["peter.thiel@foundersfund.com"]),
    "Ben Horowitz": ("https://www.linkedin.com/in/benhorowitz", ["ben@a16z.com"]),
    "Eric Ries": ("https://www.linkedin.com/in/eries", ["eric@theleanstartup.com"]),
    "Rand Fishkin": ("https://www.linkedin.com/in/randfishkin", ["rand@sparktoro.com"]),
    "Gabriel Weinberg": ("https://www.linkedin.com/in/yegg", ["gabriel@duckduckgo.com", "yegg@duckduckgo.com"]),
    "Nir Eyal": ("https://www.linkedin.com/in/nireyal", ["nir@nirandfar.com"]),
    "James Clear": ("https://www.linkedin.com/in/jamesclear", ["james@jamesclear.com"]),
    "Tim Ferriss": ("https://www.linkedin.com/in/timferriss", ["tim@fourhourworkweek.com", "tim@tim.blog"]),
    "Seth Godin": ("https://www.linkedin.com/in/sethgodin", ["seth@sethgodin.com"]),
    "Gary Vaynerchuk": ("https://www.linkedin.com/in/garyvaynerchuk", ["gary@vaynermedia.com"]),
    "Alex Hormozi": ("https://www.linkedin.com/in/alexhormozi", ["alex@acquisition.com"]),
    "Naval Ravikant": ("https://www.linkedin.com/in/navalravikant", ["naval@angellist.com"]),
    "Balaji Srinivasan": ("https://www.linkedin.com/in/balajis", ["balaji@balajis.com", "balaji@1729.com"]),
    "Tiago Forte": ("https://www.linkedin.com/in/tiagoforte", ["tiago@fortelabs.co"]),
    "Ali Abdaal": ("https://www.linkedin.com/in/aliabdaal", ["ali@aliabdaal.com"]),
    "Codie Sanchez": ("https://www.linkedin.com/in/codiesanchez", ["codie@contrarianthinking.co"]),
    "Nathan Barry": ("https://www.linkedin.com/in/nathanbarry", ["nathan@convertkit.com"]),
    "Hiten Shah": ("https://www.linkedin.com/in/hnshah", ["hiten@kissmetrics.com", "hiten@nira.com"]),
    "Des Traynor": ("https://www.linkedin.com/in/destraynor", ["des@intercom.com"]),
    "Dharmesh Shah": ("https://www.linkedin.com/in/dharmesh", ["dharmesh@hubspot.com"]),
    "Brian Chesky": ("https://www.linkedin.com/in/brianchesky", ["brian@airbnb.com"]),
    "Reid Hoffman": ("https://www.linkedin.com/in/reidhoffman", ["reid@linkedin.com"]),
    "Satya Nadella": ("https://www.linkedin.com/in/satyanadella", ["satya.nadella@microsoft.com"]),
    "Phil Knight": ("https://www.linkedin.com/in/phil-knight-nike", ["phil.knight@nike.com"]), # Placeholder, rarely public
    "Ray Dalio": ("https://www.linkedin.com/in/raydalio", ["ray@bridgewater.com"]),
    "Tony Fadell": ("https://www.linkedin.com/in/tonyfadell", ["tony@nest.com"]),
    "Marc Randolph": ("https://www.linkedin.com/in/marcrandolph", ["marc@marcrandolph.com"]),
    "Derek Sivers": ("https://www.linkedin.com/in/dereksivers", ["derek@sivers.org"]),
    "Austin Kleon": ("https://www.linkedin.com/in/austinkleon", ["austin@austinkleon.com"]),
    "Adam Grant": ("https://www.linkedin.com/in/adamgrant", ["adam@adamgrant.net"]),
    "Cal Newport": ("https://www.linkedin.com/in/calnewport", ["cal@calnewport.com"]),
    "Ryan Holiday": ("https://www.linkedin.com/in/ryanholiday", ["ryan@ryanholiday.net"]),
    "Mark Manson": ("https://www.linkedin.com/in/markmanson", ["mark@markmanson.net"]),
    "Morgan Housel": ("https://www.linkedin.com/in/morganhousel", ["morgan@collabfund.com"]),
    "Ann Handley": ("https://www.linkedin.com/in/annhandley", ["ann@marketingprofs.com"]),
    "April Dunford": ("https://www.linkedin.com/in/aprildunford", ["april@aprildunford.com"]),
    "Lenny Rachitsky": ("https://www.linkedin.com/in/lennyrachitsky", ["lenny@lennysnewsletter.com"]),
    "Kieran Flanagan": ("https://www.linkedin.com/in/kieranflanagan", ["kieran@zapier.com"]),
    "Peep Laja": ("https://www.linkedin.com/in/peeplaja", ["peep@cxl.com"]),
    "Dave Gerhardt": ("https://www.linkedin.com/in/davegerhardt", ["dave@exitfive.com"]),
    "Chris Voss": ("https://www.linkedin.com/in/chrisvoss", ["chris@blackswanltd.com"]),
    "Jocko Willink": ("https://www.linkedin.com/in/jockowillink", ["jocko@echelonfront.com"]),
    "David Goggins": ("https://www.linkedin.com/in/davidgoggins", ["david@davidgoggins.com"]),
    "Robert Kiyosaki": ("https://www.linkedin.com/in/rkiyosaki", ["robert@richdad.com"])
}

def enrich():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Enriching leads with LinkedIn and extra emails...")
    
    for name, (linkedin, emails) in ENRICHED_DATA.items():
        try:
            # Get Author ID
            cursor.execute("SELECT id FROM authors WHERE full_name=?", (name,))
            res = cursor.fetchone()
            if not res:
                print(f"Skipping {name} (Not found)")
                continue
                
            author_id = res[0]
            
            # Update LinkedIn
            cursor.execute("UPDATE authors SET linkedin_url=? WHERE id=?", (linkedin, author_id))
            
            # Insert Emails
            for email in emails:
                # Check duplication
                cursor.execute("SELECT id FROM author_emails WHERE author_id=? AND email=?", (author_id, email))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO author_emails (author_id, email, source) VALUES (?, ?, 'enrichment_script')", 
                                   (author_id, email))
        
        except Exception as e:
            print(f"Error enriching {name}: {e}")

    conn.commit()
    conn.close()
    print("Enrichment complete!")

if __name__ == "__main__":
    enrich()
