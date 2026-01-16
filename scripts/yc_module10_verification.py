import json
import requests
import re
import random
import time
import subprocess
import concurrent.futures

DATA_FILE = r'c:\Users\mohit\OneDrive\Desktop\Development\n8n Build Club Outreach\datasets\yc_hidden_gems_massive.json'

def check_mx_records(domain):
    try:
        # Use nslookup on Windows
        result = subprocess.run(
            ['nslookup', '-q=mx', domain], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        if "mail exchanger" in result.stdout:
            return True
        return False
    except Exception:
        return False

def fetch_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except:
        return ""

def verify_email_deep(url_base, target_email):
    if not url_base.startswith('http'):
        url_base = 'https://' + url_base
        
    # 1. Check Homepage
    text = fetch_url(url_base).lower()
    if target_email.lower() in text:
        return "Found on Homepage"
        
    # 2. Check Common Pages
    for path in ['/contact', '/about', '/team', '/company']:
        text = fetch_url(url_base + path).lower()
        if target_email.lower() in text:
            return f"Found on {path}"
            
    return "Not Found on Web"

def process_prospect(p):
    email = p.get('email', '')
    if not email:
        return None
        
    domain = email.split('@')[-1]
    company_url = f"www.{domain}"
    
    # Check 1: MX Records (Domain Validity)
    mx_valid = check_mx_records(domain)
    
    # Check 2: Web Scraping (Specific Email Existence)
    web_status = verify_email_deep(company_url, email)
    
    return {
        "name": p['name'],
        "email": email,
        "mx_valid": mx_valid,
        "web_status": web_status
    }

def main():
    print("Loading data...")
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        
    sample_size = 20
    sample = random.sample(data, sample_size)
    print(f"Verifying {sample_size} random prospects (Deep Check)...")
    print("-" * 60)
    print(f"{'Name':<20} | {'Email':<30} | {'MX':<5} | {'Web Check'}")
    print("-" * 60)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_prospect, sample))
        
    for r in results:
        if r:
            mx_str = "OK" if r['mx_valid'] else "FAIL"
            print(f"{r['name'][:20]:<20} | {r['email'][:30]:<30} | {mx_str:<5} | {r['web_status']}")

    print("-" * 60)
    print("Optimization: Used ThreadPool for speed.")

if __name__ == "__main__":
    main()
