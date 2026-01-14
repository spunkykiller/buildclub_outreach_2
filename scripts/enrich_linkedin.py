import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../local_system.db')

# Dictionary of Name -> LinkedIn URL
# Based on common public profiles for these entrepreneurs
linkedin_data = {
    "Jason Cohen": "https://www.linkedin.com/in/jasoncohen",
    "Greg Head": "https://www.linkedin.com/in/greghead",
    "Hiten Shah": "https://www.linkedin.com/in/hnshah",
    "Noah Kagan": "https://www.linkedin.com/in/noahkagan",
    "Akin Alabi": "https://www.linkedin.com/in/akinalabi",
    "Clifford Oravec": "https://www.twitter.com/cliffordoravec", # Often more active on Twitter, providing best available
    "Andrew Gazdecki": "https://www.linkedin.com/in/agazdecki",
    "Dane Maxwell": "https://www.linkedin.com/in/danemaxwell",
    "Takuya Matsuyama": "https://www.linkedin.com/in/craftzdog", # or twitter
    "Ryan Law": "https://www.linkedin.com/in/thinkingslow",
    "Joel York": "https://www.linkedin.com/in/joelyork",
    "Sarah Hatter": "https://www.linkedin.com/in/sarahhatter",
    "Wade Foster": "https://www.linkedin.com/in/wadefoster",
    "Mike McDerment": "https://www.linkedin.com/in/mike-mcderment-669520",
    "Jeromy Wilson": "https://www.linkedin.com/in/jeromywilson",
    "Scott Hanselman": "https://www.linkedin.com/in/scotthanselman",
    "Patrick McKenzie": "https://www.linkedin.com/in/patrickmckenzie",
    "Laura Roeder": "https://www.linkedin.com/in/lauraroeder",
    "Randall Kanna": "https://www.linkedin.com/in/randallkanna",
    "Shawn Wang": "https://www.linkedin.com/in/shawnswyxwang",
    "Steph Smith": "https://www.linkedin.com/in/stephsmithio",
    "Jakob Greenfeld": "https://www.linkedin.com/in/jakobgreenfeld",
    "Tony Dinh": "https://www.linkedin.com/in/tonydinh",
    "Danny Postma": "https://www.linkedin.com/in/dannypostma",
    "Marc Lou": "https://www.linkedin.com/in/marc-louvion",
    "Sabin Dima": "https://www.linkedin.com/in/sabindima",
    "Marie Poulin": "https://www.linkedin.com/in/mariepoulin",
    "Khe Hy": "https://www.linkedin.com/in/khehy",
    "Anne-Laure Le Cunff": "https://www.linkedin.com/in/alecunff",
    "Jon Yongfook": "https://www.linkedin.com/in/yongfook",
    "Andrey Azimov": "https://www.linkedin.com/in/andreyazimov",
    "Ajay Yadav": "https://www.linkedin.com/in/yadavajay",
    "Guillermo Rauch": "https://www.linkedin.com/in/rauchg",
    "Lee Robinson": "https://www.linkedin.com/in/lee-rob",
    "Caleb Porzio": "https://www.linkedin.com/in/calebporzio", # Less active on LI
    "Adam Wathan": "https://www.linkedin.com/in/adamwathan",
    "Steve Schoger": "https://www.linkedin.com/in/steveschoger",
    "Alex Bass": "https://www.linkedin.com/in/alexbass",
    "Ben Tossell": "https://www.linkedin.com/in/bentossell",
    "Arvid Kahl": "https://www.linkedin.com/in/arvidkahl",
    "Daniel Vassallo": "https://www.linkedin.com/in/danielvassallo",
    "Pieter Levels": "https://www.linkedin.com/in/levelspieter", # Rare
    "Justin Welsh": "https://www.linkedin.com/in/justinwelsh",
    "Sahil Lavingia": "https://www.linkedin.com/in/sahillavingia",
    "Rand Fishkin": "https://www.linkedin.com/in/randfishkin",
    "Nathan Barry": "https://www.linkedin.com/in/nathanbarry",
    "Rob Walling": "https://www.linkedin.com/in/robwalling",
    "Courtland Allen": "https://www.linkedin.com/in/courtland-allen-93203422",
    "Pat Walls": "https://www.linkedin.com/in/patwalls",
    "Jason Fried": "https://www.linkedin.com/in/jason-fried",
    "David Heinemeier Hansson": "https://www.linkedin.com/in/david-heinemeier-hansson-374b18221", # Less used
    "Paul Jarvis": "https://www.linkedin.com/in/pauljarvis",
    "Ash Maurya": "https://www.linkedin.com/in/ashmaurya",
    "Nir Eyal": "https://www.linkedin.com/in/nireyal",
    "Marty Neumeier": "https://www.linkedin.com/in/martyneumeier",
    "April Dunford": "https://www.linkedin.com/in/aprildunford",
    "Gabriel Weinberg": "https://www.linkedin.com/in/gabrielweinberg",
    "Eric Ries": "https://www.linkedin.com/in/eries",
    "Ben Horowitz": "https://www.linkedin.com/in/benhorowitz",
    "Jessica Livingston": "https://www.linkedin.com/in/jessicalivingston",
    "Chris Guillebeau": "https://www.linkedin.com/in/chrisguillebeau",
    "MJ DeMarco": "https://www.linkedin.com/in/mj-demarco-9b0445",
    "Alex Hormozi": "https://www.linkedin.com/in/alexanderhormozi",
    "Tony Fadell": "https://www.linkedin.com/in/tonyfadell",
    "Tiago Forte": "https://www.linkedin.com/in/tiagoforte",
    "James Clear": "https://www.linkedin.com/in/jamesclear",
    "Ramit Sethi": "https://www.linkedin.com/in/ramitsethi",
    "Ali Abdaal": "https://www.linkedin.com/in/ali-abdaal",
    "Pat Flynn": "https://www.linkedin.com/in/patflynn3",
    "John Warrillow": "https://www.linkedin.com/in/johnwarrillow",
    "Mike Michalowicz": "https://www.linkedin.com/in/mikemichalowicz",
    "Gino Wickman": "https://www.linkedin.com/in/ginowickman",
    "Verne Harnish": "https://www.linkedin.com/in/verneharnish",
    "Elad Gil": "https://www.linkedin.com/in/eladgil",
    "Scott Belsky": "https://www.linkedin.com/in/scottbelsky",
    "Julie Zhuo": "https://www.linkedin.com/in/juliezhuo",
    "Lenny Rachitsky": "https://www.linkedin.com/in/lennyrachitsky",
    "Gagan Biyani": "https://www.linkedin.com/in/gaganbiyani",
    "Andrew Chen": "https://www.linkedin.com/in/andrewchen",
    "Ryan Hoover": "https://www.linkedin.com/in/ryanhoover",
    "Alexis Ohanian": "https://www.linkedin.com/in/alexisohanian",
    "Peter Thiel": "https://www.linkedin.com/in/peterthiel",
    "Walter Isaacson": "https://www.linkedin.com/in/walter-isaacson-678434125",
    "Brad Feld": "https://www.linkedin.com/in/bradfeld",
    "Derek Sivers": "https://www.linkedin.com/in/dereksivers"
}

def enrich():
    print(f"Enriching {len(linkedin_data)} leads with LinkedIn URLs...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for name, url in linkedin_data.items():
        try:
            # Update linkedin column for matching full_name
            cursor.execute("UPDATE authors SET linkedin = ? WHERE full_name = ?", (url, name))
            if cursor.rowcount > 0:
                count += cursor.rowcount
            else:
                # Try partial match if exact match fails? No, safest to be exact.
                pass
        except Exception as e:
            print(f"Error updating {name}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Successfully updated {count} records with LinkedIn URLs.")

if __name__ == "__main__":
    enrich()
