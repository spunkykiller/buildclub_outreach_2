"""
YC Directory Analysis - Module 6: Integration Preparation
Prepares top YC prospects for integration into the main outreach tool.
"""

import pandas as pd
import json
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INPUT_FILE = DATA_DIR / "yc_founders_top_recent.csv"
OUTPUT_FILE = DATA_DIR / "yc_prospects_for_integration.json"

def prepare_for_integration(df):
    """Prepare top YC prospects for integration."""
    print("Preparing YC prospects for integration...")
    
    # Select top 100 prospects (highest scores)
    top_100 = df.nlargest(100, 'score').copy()
    
    print(f"Selected top {len(top_100)} prospects for integration")
    
    # Format for index.html integration
    prospects = []
    start_id = 233  # Continue from last ID in index.html
    
    for idx, row in top_100.iterrows():
        prospect = {
            'id': start_id,
            'name': row['founder_name'],
            'company': row['company_name'],
            'email': row['email_estimated'] if pd.notna(row['email_estimated']) else None,
            'linkedin': row['linkedin_profile_estimated'],
            'bio': f"{row['short_description'][:100]}... YC {row['batch']}",
            'score': int(row['score'] / 10),  # Convert to 1-10 scale
            'probability': row['podcast_potential'],
            'yc_directory': True,
            'yc_batch': row['batch'],
            'podcast_score': int(row['score'])
        }
        prospects.append(prospect)
        start_id += 1
    
    return prospects

def save_integration_data(prospects):
    """Save prospects for integration."""
    # Save as JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(prospects, f, indent=2)
    
    print(f"\nIntegration data saved to: {OUTPUT_FILE}")
    
    # Print sample
    print("\n--- Sample Prospects for Integration ---")
    for p in prospects[:10]:
        print(f"ID {p['id']}: {p['name']} ({p['company']}) - Score: {p['score']}/10, Podcast: {p['podcast_score']}/100")
    
    # Generate JavaScript array for direct copy-paste
    js_file = DATA_DIR / "yc_prospects_javascript.txt"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write("// YC Directory Prospects - Add to mainList in index.html\n\n")
        for p in prospects:
            email_str = f'"{p["email"]}"' if p['email'] else 'null'
            # Escape special characters in bio
            bio_clean = p["bio"].replace('"', '\\"').replace('\n', ' ').encode('ascii', 'ignore').decode('ascii')
            f.write(f'{{ id: {p["id"]}, name: "{p["name"]}", company: "{p["company"]}", ')
            f.write(f'email: {email_str}, linkedin: "{p["linkedin"]}", ')
            f.write(f'bio: "{bio_clean}", score: {p["score"]}, probability: "{p["probability"]}", ')
            f.write(f'yc_directory: true, yc_batch: "{p["yc_batch"]}", podcast_score: {p["podcast_score"]} }},\n')
    
    print(f"JavaScript code saved to: {js_file}")
    
    return prospects

def generate_summary_stats(prospects):
    """Generate summary statistics."""
    print("\n" + "="*60)
    print("INTEGRATION SUMMARY")
    print("="*60)
    
    df = pd.DataFrame(prospects)
    
    print(f"\nTotal prospects to integrate: {len(prospects)}")
    print(f"ID range: {df['id'].min()} to {df['id'].max()}")
    
    print("\n--- Score Distribution ---")
    print(f"Average score: {df['score'].mean():.1f}/10")
    print(f"Median score: {df['score'].median():.0f}/10")
    
    print("\n--- Podcast Score Distribution ---")
    print(f"Average podcast score: {df['podcast_score'].mean():.1f}/100")
    
    print("\n--- Probability Distribution ---")
    for prob in df['probability'].value_counts().items():
        print(f"{prob[0]}: {prob[1]} prospects")
    
    print("\n--- Batch Distribution ---")
    for batch in df['yc_batch'].value_counts().head(5).items():
        print(f"{batch[0]}: {batch[1]} prospects")
    
    print("\n--- Email Coverage ---")
    with_email = df['email'].notna().sum()
    print(f"With email: {with_email} ({with_email/len(df)*100:.1f}%)")

if __name__ == "__main__":
    # Load top recent prospects
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Prepare for integration
    prospects = prepare_for_integration(df)
    
    # Save
    prospects = save_integration_data(prospects)
    
    # Generate summary
    generate_summary_stats(prospects)
    
    print("\n" + "="*60)
    print("MODULE 6 PREPARATION COMPLETE")
    print("="*60)
    print("\nNext: Update index.html to add YC Directory column and import prospects")
