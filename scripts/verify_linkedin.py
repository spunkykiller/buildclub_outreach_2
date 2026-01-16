import json
import re

DATA_FILE = r'c:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets\yc_hidden_gems_massive.json'

def verify_linkedin_format(url):
    if not url: return "Missing"
    # Basic check for linkedin.com/in/
    if not re.search(r'linkedin\.com/in/[\w-]+', url):
        return "Invalid Format"
    return "Valid Format"

def main():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    print(f"Checking LinkedIn URLs for {len(data)} prospects...")
    print("-" * 40)

    stats = {"Valid": 0, "Invalid": 0, "Missing": 0}
    invalid_samples = []
    sample_urls = []

    for i, p in enumerate(data):
        status = verify_linkedin_format(p.get('linkedin', ''))
        if status == "Valid Format":
            stats["Valid"] += 1
            if i % 500 == 0: # Grab a few spread out for manual check
                sample_urls.append(p.get('linkedin'))
        elif status == "Missing":
            stats["Missing"] += 1
        else:
            stats["Invalid"] += 1
            if len(invalid_samples) < 5:
                invalid_samples.append((p['name'], p.get('linkedin')))

    print(f"Results: {stats}")
    if invalid_samples:
        print("\nInvalid Sample:")
        for name, url in invalid_samples:
            print(f"  {name}: {url}")
    else:
        print("\nAll formats are valid!")
        
    print("\nRecommended for Manual Verification:")
    for url in sample_urls:
        print(url)

if __name__ == "__main__":
    main()
