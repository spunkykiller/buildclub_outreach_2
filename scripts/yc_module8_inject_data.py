"""
YC Directory Analysis - Module 8: Inject Data
Safely injects massive dataset into index.html.
"""

import json
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INDEX_FILE = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\index.html")
INPUT_FILE = DATA_DIR / "yc_hidden_gems_massive.json"

def inject_data():
    """Inject massive dataset into index.html."""
    print("Injecting massive dataset into index.html...")
    
    # Load new prospects
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        prospects = json.load(f)
    print(f"Loaded {len(prospects)} new prospects")
    
    # Read index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Locate insertion point (end of mainList)
    # We look for the closing bracket of mainList
    # It ends with specific existing entries, so let's find the closing bracket
    # The last entry we added was ID 332 (Kurtis Tryber)
    
    marker = '{ id: 332, name: "Kurtis Tryber"'
    if marker not in content:
        print("Error: Could not find insertion marker (ID 332)")
        return
    
    # Find the end of that line/object
    insert_pos = content.find(marker)
    # Find the next closing bracket ']' which closes mainList
    main_list_end = content.find(']', insert_pos)
    
    if main_list_end == -1:
        print("Error: Could not find end of mainList")
        return
    
    # Prepare injection string
    injection = ",\n                        // MASSIVE IMPORT: YC Hidden Gems (1600+ founders)\n"
    
    for p in prospects:
        email_str = f'"{p["email"]}"' if p['email'] else 'null'
        # Escape bio and name
        bio_clean = p["bio"].replace('"', '\\"').replace('\n', ' ').strip()
        name_clean = p["name"].replace('"', '\\"')
        company_clean = p["company"].replace('"', '\\"')
        
        line = f'                        {{ id: {p["id"]}, name: "{name_clean}", company: "{company_clean}", '
        line += f'email: {email_str}, linkedin: "{p["linkedin"]}", '
        line += f'bio: "{bio_clean}", score: {p["score"]}, probability: "{p["probability"]}", '
        line += f'yc_directory: true, yc_batch: "{p["yc_batch"]}", podcast_score: {p["podcast_score"]} }},\n'
        injection += line
    
    # Remove the last comma/newline if needed, but since we are inserting BEFORE the closing bracket, 
    # and the previous item (ID 332) didn't have a trailing comma in the file (it was usually last), 
    # we need to ensure ID 332 adds a comma.
    
    # Let's check if there is a comma after ID 332
    # Actually, in JS array, trailing comma is allowed.
    # But we need to make sure we append correctly.
    
    # Strategy: Replace the substring from ID 332 to the end of its line
    # with ID 332 + comma + new lines
    
    # Find end of ID 332 object
    id332_start = content.find(marker)
    id332_end = content.find('}', id332_start) + 1
    
    # Insert AFTER ID 332
    new_content = content[:id332_end] + injection.rstrip(',\n') + content[id332_end:]
    
    # Write back
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("Injection complete!")
    print(f"Total prospects should now be: {332 + len(prospects)}")

if __name__ == "__main__":
    inject_data()
