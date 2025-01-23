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
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'href'])
        writer.writeheader()
        writer.writerows(data)
    print(f"Results saved to {filepath}")

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
