"""
YC Directory Analysis - Module 3: LinkedIn Enrichment
Enriches founder data with LinkedIn profiles using available company data and name patterns.
"""

import pandas as pd
import re
from pathlib import Path
from urllib.parse import urlparse

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INPUT_FILE = DATA_DIR / "yc_founders_extracted.csv"
OUTPUT_FILE = DATA_DIR / "yc_founders_linkedin_enriched.csv"

def clean_founder_names(df):
    """Clean founder names (remove brackets and extra characters)."""
    print("Cleaning founder names...")
    
    # Remove brackets and quotes
    df['founder_name'] = df['founder_name'].str.replace(r"[\[\]'\"]", '', regex=True)
    df['founder_name'] = df['founder_name'].str.strip()
    
    # Filter out invalid names
    df = df[df['founder_name'].str.len() > 2]
    df = df[~df['founder_name'].str.contains(r'^\d+$', na=False)]
    
    print(f"Cleaned {len(df)} founder names")
    return df

def generate_linkedin_slug(name):
    """Generate a likely LinkedIn profile slug from a name."""
    # Convert to lowercase, replace spaces with hyphens
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'-+', '-', slug)  # Remove multiple hyphens
    return slug

def enrich_with_linkedin(df):
    """Enrich founders with LinkedIn profile URLs."""
    print("\nEnriching with LinkedIn data...")
    
    # Generate likely LinkedIn URLs
    df['linkedin_slug'] = df['founder_name'].apply(generate_linkedin_slug)
    df['linkedin_profile_estimated'] = 'https://www.linkedin.com/in/' + df['linkedin_slug']
    
    # Mark if we have company LinkedIn
    df['has_company_linkedin'] = df['company_linkedin'].notna()
    
    # LinkedIn confidence score
    # High: Has company LinkedIn + clean name
    # Medium: Clean name only
    # Low: Unclear name pattern
    
    def calculate_linkedin_confidence(row):
        if row['has_company_linkedin'] and len(row['founder_name'].split()) >= 2:
            return 'High'
        elif len(row['founder_name'].split()) >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    df['linkedin_confidence'] = df.apply(calculate_linkedin_confidence, axis=1)
    
    print(f"High confidence: {(df['linkedin_confidence'] == 'High').sum()}")
    print(f"Medium confidence: {(df['linkedin_confidence'] == 'Medium').sum()}")
    print(f"Low confidence: {(df['linkedin_confidence'] == 'Low').sum()}")
    
    return df

def prioritize_recent_batches(df):
    """Prioritize recent batches for manual verification."""
    print("\nPrioritizing recent batches...")
    
    recent_batches = ['W22', 'S22', 'W23', 'S23', 'W24', 'S24']
    df['is_recent_batch'] = df['batch'].isin(recent_batches)
    
    recent_df = df[df['is_recent_batch']].copy()
    print(f"Recent batch founders: {len(recent_df)}")
    
    # Further prioritize by industry
    priority_industries = ['AI', 'Artificial Intelligence', 'Developer Tools', 'SaaS', 'B2B']
    recent_df['is_priority_industry'] = recent_df['tags'].str.contains('|'.join(priority_industries), case=False, na=False)
    
    priority_df = recent_df[recent_df['is_priority_industry']].copy()
    print(f"Priority industry founders (recent batches): {len(priority_df)}")
    
    return df, recent_df, priority_df

def save_enriched_data(df, recent_df, priority_df):
    """Save enriched data."""
    # Save all founders
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nAll enriched founders saved to: {OUTPUT_FILE}")
    
    # Save recent batch founders
    recent_file = DATA_DIR / "yc_founders_recent_enriched.csv"
    recent_df.to_csv(recent_file, index=False)
    print(f"Recent batch founders saved to: {recent_file}")
    
    # Save priority founders (recent + priority industry)
    priority_file = DATA_DIR / "yc_founders_priority.csv"
    priority_df.to_csv(priority_file, index=False)
    print(f"Priority founders saved to: {priority_file}")
    
    # Print sample
    print("\n--- Sample Priority Founders ---")
    sample_cols = ['founder_name', 'company_name', 'batch', 'linkedin_profile_estimated', 'linkedin_confidence']
    print(priority_df[sample_cols].head(15).to_string())
    
    # Statistics
    print("\n--- LinkedIn Enrichment Stats ---")
    print(f"Total founders: {len(df)}")
    print(f"With company LinkedIn: {df['has_company_linkedin'].sum()} ({df['has_company_linkedin'].sum()/len(df)*100:.1f}%)")
    print(f"High confidence LinkedIn: {(df['linkedin_confidence'] == 'High').sum()}")
    print(f"Medium confidence LinkedIn: {(df['linkedin_confidence'] == 'Medium').sum()}")

if __name__ == "__main__":
    # Load extracted founder data
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Clean names
    df = clean_founder_names(df)
    
    # Enrich with LinkedIn
    df = enrich_with_linkedin(df)
    
    # Prioritize recent batches
    all_df, recent_df, priority_df = prioritize_recent_batches(df)
    
    # Save
    save_enriched_data(all_df, recent_df, priority_df)
    
    print("\n" + "="*60)
    print("MODULE 3 COMPLETE")
    print("="*60)
    print("\nNote: LinkedIn URLs are estimated based on name patterns.")
    print("Manual verification recommended for high-priority founders.")
