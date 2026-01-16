"""
YC Directory Analysis - Module 1: Data Discovery & Loading
Loads and merges YC company datasets for podcast outreach analysis.
"""

import pandas as pd
import json
from pathlib import Path

# Paths
DATA_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")
OUTPUT_DIR = Path(r"C:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets")

def load_yc_datasets():
    """Load and merge both YC company datasets."""
    print("Loading YC datasets...")
    
    # Load both CSV files
    df1 = pd.read_csv(DATA_DIR / "2023-02-27-yc-companies.csv")
    df2 = pd.read_csv(DATA_DIR / "2023-07-13-yc-companies.csv")
    
    print(f"Dataset 1 (2023-02-27): {len(df1)} companies")
    print(f"Dataset 2 (2023-07-13): {len(df2)} companies")
    
    # Merge datasets, keeping the most recent data for duplicates
    merged = pd.concat([df1, df2], ignore_index=True)
    
    # Remove duplicates based on company_id, keeping the last occurrence (most recent)
    merged = merged.drop_duplicates(subset=['company_id'], keep='last')
    
    print(f"Merged dataset: {len(merged)} unique companies")
    
    return merged

def analyze_dataset(df):
    """Analyze the merged dataset and print summary statistics."""
    print("\n" + "="*60)
    print("DATASET ANALYSIS")
    print("="*60)
    
    # Basic stats
    print(f"\nTotal Companies: {len(df)}")
    print(f"Total Founders: {df['num_founders'].sum():.0f}")
    print(f"Average Founders per Company: {df['num_founders'].mean():.2f}")
    
    # Batch distribution
    print("\n--- Batch Distribution (Top 10) ---")
    batch_counts = df['batch'].value_counts().head(10)
    for batch, count in batch_counts.items():
        print(f"{batch}: {count} companies")
    
    # Status distribution
    print("\n--- Status Distribution ---")
    status_counts = df['status'].value_counts()
    for status, count in status_counts.items():
        print(f"{status}: {count} companies")
    
    # Tags/Industries (top 10)
    print("\n--- Top 10 Industries/Tags ---")
    all_tags = []
    for tags in df['tags'].dropna():
        if isinstance(tags, str):
            all_tags.extend([t.strip() for t in tags.split(',')])
    
    from collections import Counter
    tag_counts = Counter(all_tags).most_common(10)
    for tag, count in tag_counts:
        print(f"{tag}: {count} companies")
    
    # LinkedIn coverage
    linkedin_coverage = df['linkedin_url'].notna().sum()
    print(f"\n--- LinkedIn Coverage ---")
    print(f"Companies with LinkedIn: {linkedin_coverage} ({linkedin_coverage/len(df)*100:.1f}%)")
    
    # Founders with names
    founders_with_names = df['founders_names'].notna().sum()
    print(f"\n--- Founder Data ---")
    print(f"Companies with founder names: {founders_with_names} ({founders_with_names/len(df)*100:.1f}%)")
    
    # Recent batches (W22 onwards)
    recent_batches = ['W22', 'S22', 'W23', 'S23', 'W24', 'S24']
    recent_df = df[df['batch'].isin(recent_batches)]
    print(f"\n--- Recent Batches (W22-S24) ---")
    print(f"Companies: {len(recent_df)}")
    
    return df

def save_summary(df):
    """Save a summary of the dataset."""
    summary = {
        'total_companies': len(df),
        'total_founders': int(df['num_founders'].sum()),
        'batches': df['batch'].value_counts().to_dict(),
        'linkedin_coverage': int(df['linkedin_url'].notna().sum()),
        'founder_names_available': int(df['founders_names'].notna().sum())
    }
    
    output_file = OUTPUT_DIR / "yc_dataset_summary.json"
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to: {output_file}")
    
    # Save merged dataset
    merged_file = OUTPUT_DIR / "yc_companies_merged.csv"
    df.to_csv(merged_file, index=False)
    print(f"Merged dataset saved to: {merged_file}")

if __name__ == "__main__":
    # Load datasets
    df = load_yc_datasets()
    
    # Analyze
    df = analyze_dataset(df)
    
    # Save summary
    save_summary(df)
    
    print("\n" + "="*60)
    print("MODULE 1 COMPLETE")
    print("="*60)
