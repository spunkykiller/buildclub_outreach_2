"""
YC Directory Analysis - Module 2: Data Extraction & Cleaning
Extracts individual founder records from company data.
"""

import pandas as pd
import re
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INPUT_FILE = DATA_DIR / "yc_companies_merged.csv"
OUTPUT_FILE = DATA_DIR / "yc_founders_extracted.csv"

def parse_founders(df):
    """Extract individual founder records from company data."""
    print("Extracting individual founder records...")
    
    founders_list = []
    
    for idx, row in df.iterrows():
        company_id = row['company_id']
        company_name = row['company_name']
        batch = row['batch']
        tags = row['tags'] if pd.notna(row['tags']) else ''
        status = row['status']
        founders_names = row['founders_names']
        num_founders = row['num_founders']
        linkedin_url = row['linkedin_url'] if pd.notna(row['linkedin_url']) else None
        website = row['website'] if pd.notna(row['website']) else None
        location = row['location'] if pd.notna(row['location']) else None
        short_desc = row['short_description'] if pd.notna(row['short_description']) else ''
        
        # Parse founder names (they're usually separated by commas or semicolons)
        if pd.notna(founders_names) and founders_names:
            # Split by common separators
            names = re.split(r'[,;]', str(founders_names))
            names = [name.strip() for name in names if name.strip()]
            
            for founder_name in names:
                founders_list.append({
                    'founder_name': founder_name,
                    'company_id': company_id,
                    'company_name': company_name,
                    'batch': batch,
                    'status': status,
                    'tags': tags,
                    'location': location,
                    'website': website,
                    'company_linkedin': linkedin_url,
                    'short_description': short_desc,
                    'num_founders': num_founders
                })
    
    founders_df = pd.DataFrame(founders_list)
    print(f"Extracted {len(founders_df)} individual founder records")
    
    return founders_df

def clean_founder_data(df):
    """Clean and normalize founder data."""
    print("\nCleaning founder data...")
    
    initial_count = len(df)
    
    # Remove entries with invalid names
    df = df[df['founder_name'].str.len() > 2]  # At least 3 characters
    df = df[~df['founder_name'].str.contains(r'^\d+$', na=False)]  # Not just numbers
    
    # Normalize names (title case)
    df['founder_name'] = df['founder_name'].str.title()
    
    # Remove duplicates (same founder, same company)
    df = df.drop_duplicates(subset=['founder_name', 'company_id'])
    
    print(f"Removed {initial_count - len(df)} invalid/duplicate records")
    print(f"Final count: {len(df)} founders")
    
    return df

def filter_recent_batches(df):
    """Filter for recent batches (W22-S24 priority)."""
    print("\nFiltering for recent batches...")
    
    recent_batches = ['W22', 'S22', 'W23', 'S23', 'W24', 'S24']
    recent_df = df[df['batch'].isin(recent_batches)].copy()
    
    print(f"Recent batches (W22-S24): {len(recent_df)} founders")
    print(f"All batches: {len(df)} founders")
    
    return df, recent_df

def analyze_industries(df):
    """Analyze industry distribution."""
    print("\n--- Industry Analysis ---")
    
    # Count founders by industry tags
    ai_keywords = ['AI', 'Artificial Intelligence', 'Machine Learning', 'ML']
    devtools_keywords = ['Developer Tools', 'DevOps', 'Infrastructure']
    saas_keywords = ['SaaS', 'B2B']
    
    df['is_ai'] = df['tags'].str.contains('|'.join(ai_keywords), case=False, na=False)
    df['is_devtools'] = df['tags'].str.contains('|'.join(devtools_keywords), case=False, na=False)
    df['is_saas'] = df['tags'].str.contains('|'.join(saas_keywords), case=False, na=False)
    
    print(f"AI/ML founders: {df['is_ai'].sum()}")
    print(f"DevTools founders: {df['is_devtools'].sum()}")
    print(f"SaaS/B2B founders: {df['is_saas'].sum()}")
    
    return df

def save_extracted_data(df, recent_df):
    """Save extracted founder data."""
    # Save all founders
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nAll founders saved to: {OUTPUT_FILE}")
    
    # Save recent batch founders
    recent_file = DATA_DIR / "yc_founders_recent.csv"
    recent_df.to_csv(recent_file, index=False)
    print(f"Recent batch founders saved to: {recent_file}")
    
    # Print sample
    print("\n--- Sample Records ---")
    print(df[['founder_name', 'company_name', 'batch', 'tags']].head(10).to_string())

if __name__ == "__main__":
    # Load merged company data
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Extract individual founders
    founders_df = parse_founders(df)
    
    # Clean data
    founders_df = clean_founder_data(founders_df)
    
    # Filter for recent batches
    all_founders, recent_founders = filter_recent_batches(founders_df)
    
    # Analyze industries
    all_founders = analyze_industries(all_founders)
    
    # Save
    save_extracted_data(all_founders, recent_founders)
    
    print("\n" + "="*60)
    print("MODULE 2 COMPLETE")
    print("="*60)
