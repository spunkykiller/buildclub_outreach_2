"""
YC Directory Analysis - Modules 4-5: Email Discovery & Podcast Scoring
Estimates email addresses and scores founders for podcast outreach potential.
"""

import pandas as pd
import re
from pathlib import Path
from urllib.parse import urlparse

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
INPUT_FILE = DATA_DIR / "yc_founders_linkedin_enriched.csv"
OUTPUT_FILE = DATA_DIR / "yc_founders_scored.csv"

def extract_domain_from_website(website):
    """Extract clean domain from website URL."""
    if pd.isna(website) or not website:
        return None
    
    try:
        # Parse URL
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        parsed = urlparse(website)
        domain = parsed.netloc or parsed.path
        
        # Remove www.
        domain = domain.replace('www.', '')
        
        return domain if domain else None
    except:
        return None

def generate_email_estimates(df):
    """Generate estimated email addresses for founders."""
    print("Generating email estimates...")
    
    # Extract domain from website
    df['domain'] = df['website'].apply(extract_domain_from_website)
    
    # Generate email patterns
    def create_email_patterns(row):
        if pd.isna(row['domain']) or not row['domain']:
            return None, 'Unknown'
        
        name_parts = row['founder_name'].lower().split()
        if len(name_parts) < 2:
            return None, 'Low'
        
        first = name_parts[0]
        last = name_parts[-1]
        domain = row['domain']
        
        # Most common pattern: first@domain.com
        email = f"{first}@{domain}"
        confidence = 'Medium'
        
        # Higher confidence if we have company LinkedIn
        if row['has_company_linkedin']:
            confidence = 'High'
        
        return email, confidence
    
    df[['email_estimated', 'email_confidence']] = df.apply(
        lambda row: pd.Series(create_email_patterns(row)), axis=1
    )
    
    print(f"Emails estimated: {df['email_estimated'].notna().sum()}")
    print(f"High confidence: {(df['email_confidence'] == 'High').sum()}")
    print(f"Medium confidence: {(df['email_confidence'] == 'Medium').sum()}")
    
    return df

def calculate_podcast_score(df):
    """Calculate podcast outreach score (0-100)."""
    print("\nCalculating podcast outreach scores...")
    
    df['score'] = 0
    
    # ACCESSIBILITY (40 points)
    # Has LinkedIn profile (estimated): +20
    df.loc[df['linkedin_confidence'].isin(['High', 'Medium']), 'score'] += 20
    
    # Has email estimate: +15
    df.loc[df['email_estimated'].notna(), 'score'] += 15
    
    # Recent batch (W24/S24): +5
    df.loc[df['batch'].isin(['W24', 'S24']), 'score'] += 5
    
    # RELEVANCE (30 points)
    # AI/ML industry: +15
    df.loc[df['is_ai'] == True, 'score'] += 15
    
    # DevTools industry: +10
    df.loc[df['is_devtools'] == True, 'score'] += 10
    
    # SaaS/B2B: +5
    df.loc[df['is_saas'] == True, 'score'] += 5
    
    # ENGAGEMENT POTENTIAL (30 points)
    # Active company (not inactive): +15
    df.loc[df['status'] == 'Active', 'score'] += 15
    
    # Has company LinkedIn (shows online presence): +10
    df.loc[df['has_company_linkedin'] == True, 'score'] += 10
    
    # Multiple founders (collaborative culture): +5
    df.loc[df['num_founders'] >= 2, 'score'] += 5
    
    # Categorize scores
    def categorize_score(score):
        if score >= 80:
            return 'Very High'
        elif score >= 60:
            return 'High'
        elif score >= 40:
            return 'Medium'
        else:
            return 'Low'
    
    df['podcast_potential'] = df['score'].apply(categorize_score)
    
    # Print distribution
    print("\n--- Podcast Potential Distribution ---")
    for category in ['Very High', 'High', 'Medium', 'Low']:
        count = (df['podcast_potential'] == category).sum()
        print(f"{category}: {count} founders ({count/len(df)*100:.1f}%)")
    
    print(f"\nAverage score: {df['score'].mean():.1f}/100")
    print(f"Median score: {df['score'].median():.0f}/100")
    
    return df

def filter_top_prospects(df):
    """Filter and rank top podcast prospects."""
    print("\nFiltering top prospects...")
    
    # Filter for High and Very High potential
    top_df = df[df['podcast_potential'].isin(['High', 'Very High'])].copy()
    
    # Sort by score (descending)
    top_df = top_df.sort_values('score', ascending=False)
    
    print(f"Top prospects (High/Very High): {len(top_df)}")
    
    # Further filter for recent batches
    top_recent = top_df[top_df['is_recent_batch'] == True].copy()
    print(f"Top prospects (recent batches): {len(top_recent)}")
    
    return top_df, top_recent

def save_scored_data(df, top_df, top_recent_df):
    """Save scored data."""
    # Save all scored founders
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nAll scored founders saved to: {OUTPUT_FILE}")
    
    # Save top prospects
    top_file = DATA_DIR / "yc_founders_top_prospects.csv"
    top_df.to_csv(top_file, index=False)
    print(f"Top prospects saved to: {top_file}")
    
    # Save top recent prospects
    top_recent_file = DATA_DIR / "yc_founders_top_recent.csv"
    top_recent_df.to_csv(top_recent_file, index=False)
    print(f"Top recent prospects saved to: {top_recent_file}")
    
    # Print sample of top prospects
    print("\n--- Top 20 Podcast Prospects ---")
    sample_cols = ['founder_name', 'company_name', 'batch', 'score', 'podcast_potential', 
                   'email_estimated', 'linkedin_profile_estimated']
    print(top_df[sample_cols].head(20).to_string(index=False))

if __name__ == "__main__":
    # Load enriched data
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Generate email estimates
    df = generate_email_estimates(df)
    
    # Calculate podcast scores
    df = calculate_podcast_score(df)
    
    # Filter top prospects
    top_df, top_recent_df = filter_top_prospects(df)
    
    # Save
    save_scored_data(df, top_df, top_recent_df)
    
    print("\n" + "="*60)
    print("MODULES 4-5 COMPLETE")
    print("="*60)
