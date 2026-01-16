"""
YC Directory Analysis - Module 8: Massive "Hidden Gem" Import
Selects ALL eligible founders from recent batches for massive import.
"""

import pandas as pd
import json
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INPUT_FILE = DATA_DIR / "yc_founders_scored.csv"
OUTPUT_FILE = DATA_DIR / "yc_hidden_gems_massive.json"

def select_hidden_gems(df):
    """Select all eligible founders from recent batches."""
    print("Selecting 'Hidden Gems' (Massive Import)...")
    
    # 1. Filter Batches (W22-S24) - The "Builders"
    recent_batches = ['W22', 'S22', 'W23', 'S23', 'W24', 'S24']
    df = df[df['batch'].isin(recent_batches)].copy()
    print(f"Founders in recent batches (W22-S24): {len(df)}")
    
    # 2. Filter Industries (Broad set for 'eligible')
    # We want AI, DevTools, SaaS, B2B, Fintech, Marketplace, Crypto, Healthcare
    # Basically anything that might need a 'Build Club' or tech outreach
    # Excluding: maybe purely 'Consumer' if unrelated to tech? But for n8n, almost any startup is relevant.
    # Let's stick to the core high-value ones first to ensure quality "Yes" probability.
    
    target_keywords = [
        'AI', 'Artificial Intelligence', 'Machine Learning', 'B2B', 'SaaS', 
        'Developer Tools', 'Fintech', 'Marketplace', 'Enterprise', 'API',
        'Data', 'Infrastructure', 'Cloud', 'Engineering'
    ]
    
    pattern = '|'.join(target_keywords)
    df['is_target'] = df['tags'].str.contains(pattern, case=False, na=False)
    
    target_df = df[df['is_target']].copy()
    print(f"Founders in target industries: {len(target_df)}")
    
    # 3. Filter for Valid Email Estimate
    # We need to be able to contact them.
    # High + Medium confidence emails.
    email_df = target_df[target_df['email_estimated'].notna()].copy()
    print(f"Founders with valid email estimates: {len(email_df)}")
    
    # 4. Exclude Very Low Scores (if any)
    # If they scored < 40, they likely lack Linkedin AND Email, or are inactive.
    # But we already filtered for email.
    # Let's check status.
    valid_status = ['Active', 'Public', 'Acquired'] # Maybe 'Inactive' is bad.
    final_df = email_df[email_df['status'].isin(valid_status)].copy()
    print(f"Founders with valid status: {len(final_df)}")
    
    return final_df

def prepare_massive_import(df):
    """Format for index.html integration."""
    print("\nPreparing massive import list...")
    
    # Sort by Score (desc) then Batch (desc)
    df = df.sort_values(['score', 'batch'], ascending=[False, False])
    
    prospects = []
    start_id = 333  # Continue from last ID in index.html (we added up to 332)
    
    # Exclude already added (top 100 recent were IDs 233-332)
    # We need to check names/linkedin to avoid duplicates with the 100 we just added.
    # Load the set of already added names/linkedins
    # For now, I'll relies on the fact that I'm taking *everyone* and I'll just skip the top 100 by logic or checking names.
    # Better: I'll generate the full list and exclude by name if possible, or just generate new IDs.
    
    # Wait, the previous step added the *top 100* by score.
    # If I sort by score here, the top 100 will be the same people.
    # I should explicitly exclude the top 100 I identified in Module 6.
    
    # Let's load the previous integration file to check IDs/Names
    prev_file = DATA_DIR / "yc_prospects_for_integration.json"
    if prev_file.exists():
        with open(prev_file, 'r') as f:
            prev_data = json.load(f)
            prev_names = set(p['name'] for p in prev_data)
            print(f"Excluding {len(prev_names)} already added founders...")
            df = df[~df['founder_name'].isin(prev_names)]
    
    print(f"Final count for import: {len(df)}")
    
    for idx, row in df.iterrows():
        # Clean bio text
        bio_text = str(row['short_description'])
        if len(bio_text) > 100:
            bio_text = bio_text[:100] + "..."
        bio_text = f"{bio_text} YC {row['batch']}"
        
        # Determine probability label
        prob = row['podcast_potential']
        if prob == 'Very High':
            prob = "Very High" # Keep as is
        elif prob == 'High':
            prob = "High"
        elif prob == 'Medium':
            prob = "Medium"
        else:
            prob = "Low"

        prospect = {
            'id': start_id,
            'name': row['founder_name'],
            'company': row['company_name'],
            'email': row['email_estimated'],
            'linkedin': row['linkedin_profile_estimated'],
            'bio': bio_text,
            'score': int(row['score'] / 10),
            'probability': prob,
            'yc_directory': True,
            'yc_batch': row['batch'],
            'podcast_score': int(row['score'])
        }
        prospects.append(prospect)
        start_id += 1
        
    return prospects

def save_massive_data(prospects):
    """Save massive data to files."""
    # JSON for safety
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(prospects, f, indent=2)
    
    print(f"\nMassive import data saved to: {OUTPUT_FILE}")
    
    # Text file for Copy-Paste (JavaScript array)
    js_file = DATA_DIR / "yc_massive_import_js.txt"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write("// MASSIVE IMPORT: YC Founders (W22-S24)\n\n")
        f.write("const newProspects = [\n")
        
        for p in prospects:
            email_str = f'"{p["email"]}"' if p['email'] else 'null'
            # Escape bio
            bio_clean = p["bio"].replace('"', '\\"').replace('\n', ' ').strip()
            
            line = f'    {{ id: {p["id"]}, name: "{p["name"]}", company: "{p["company"]}", '
            line += f'email: {email_str}, linkedin: "{p["linkedin"]}", '
            line += f'bio: "{bio_clean}", score: {p["score"]}, probability: "{p["probability"]}", '
            line += f'yc_directory: true, yc_batch: "{p["yc_batch"]}", podcast_score: {p["podcast_score"]} }},\n'
            f.write(line)
            
        f.write("];\n")
        f.write("// Add strictly to mainList: mainList.push(...newProspects);\n")
        
    print(f"JavaScript import file saved to: {js_file}")

if __name__ == "__main__":
    # Load scored data
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Select gems
    gems_df = select_hidden_gems(df)
    
    # Prepare import
    prospects = prepare_massive_import(gems_df)
    
    # Save
    save_massive_data(prospects)
    
    print("\n" + "="*60)
    print("MODULE 8 COMPLETE")
    print(f"Ready to import {len(prospects)} hidden gems!")
    print("="*60)
