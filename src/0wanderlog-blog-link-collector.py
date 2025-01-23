import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import csv

def fetch_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(html_content, base_url, selector):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for link in soup.select(selector):
        href = link.get('href', '').strip()
        text = link.get_text(strip=True)
        
        # Resolve relative URLs
        if base_url and not urlparse(href).netloc:
            href = urljoin(base_url, href)
        
        links.append({
            'text': text,
            'href': href
        })
    
    return links

def save_to_csv(data):
    filename = input("Please enter the filename to save the results (with .csv extension): ")
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
    
    # Read existing data
    existing_data = []
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    
    # Convert existing data to a set of tuples for easy comparison
    existing_set = {(row['text'], row['href']) for row in existing_data}
    
    # Filter out duplicates
    new_data = [row for row in data if (row['text'], row['href']) not in existing_set]
    
    # Append new data to the existing data
    if new_data:
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['text', 'href'])
            if not existing_data:
                writer.writeheader()
            writer.writerows(new_data)
        print(f"New results added to {filepath}")
    else:
        print("No new data to add.")

def scrape_website(url, selector):
    page_content = fetch_page(url)
    
    if page_content:
        links = extract_links(page_content, url, selector)
        save_to_csv(links)
        return links
    return []

# Example usage
if __name__ == '__main__':
    target_url = input("Please enter the URL to scrape: ")
    selector = '.row.mt-n2.mx-n1 .col-6.col-sm-4.col-md-4.col-lg-4.col-xl-4.mt-2.px-1 a'
    scrape_website(target_url, selector)
    
    # Run the cleanup script
    cleanup_script = os.path.join('src', 'output', 'remove-dupes.py')
    if os.path.exists(cleanup_script):
        os.system(f'python {cleanup_script}')
    else:
        print(f"Cleanup script {cleanup_script} not found.")
