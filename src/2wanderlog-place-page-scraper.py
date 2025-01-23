import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime
import os
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[logging.FileHandler('scraper.log'), logging.StreamHandler()]
)

# Load CSV file
def load_restaurant_links(csv_file):
    try:
        csv_path = os.path.join('output', csv_file)
        restaurants = pd.read_csv(csv_path)
        logging.info(f"Loaded {len(restaurants)} restaurant links from {csv_path}")
        return restaurants
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        raise

# Scrape restaurant data
def scrape_restaurant_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract details
        name = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'N/A'
        google_stars, google_reviews = extract_ratings(soup, 0)
        tripadvisor_stars, tripadvisor_reviews = extract_ratings(soup, 1)
        wanderlog_ranking, wanderlog_list = extract_wanderlog_ranking(soup)
        about_text = extract_about(soup)
        address, phone, website = extract_contact_info(soup)

        return {
            'Name': name,
            'Phone': phone,
            'Website': address,
            'Google Stars': google_stars,
            'Google Reviews': google_reviews,
            'TripAdvisor Stars': tripadvisor_stars,
            'TripAdvisor Reviews': tripadvisor_reviews,
            'Wanderlog Ranking': wanderlog_ranking,
            'Wanderlog List': wanderlog_list,
            'About': about_text,
            # 'Website': website,
            'Link': url
        }
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return None

# Helper functions
def extract_ratings(soup, index):
    rating_divs = soup.find_all('div', class_='d-flex flex-wrap align-items-center')
    if len(rating_divs) > index:
        stars = rating_divs[index].find('span', class_='font-weight-bold')
        reviews = rating_divs[index].find('span', class_='ml-1 text-muted')
        return (
            stars.get_text(strip=True) if stars else 'N/A',
            reviews.get_text(strip=True).strip('()') if reviews else 'N/A'
        )
    return 'N/A', 'N/A'

def extract_wanderlog_ranking(soup):
    ranking_div = soup.find('div', class_='d-flex flex-row align-items-center flex-wrap')
    if ranking_div:
        tag = ranking_div.find('a', class_='text-muted')
        if tag:
            rank = tag.find('span', class_='font-weight-bold')
            return rank.get_text(strip=True) if rank else 'N/A', tag.get_text(strip=True)
    return 'N/A', 'N/A'

def extract_about(soup):
    about_section = soup.find('div', class_='mt-5')
    if about_section:
        about_text = about_section.find_next('div')
        return about_text.get_text(strip=True) if about_text else 'N/A'
    return 'N/A'

def extract_contact_info(soup):
    address_div = soup.find('div', class_='mt-3')
    address = address_div.find('a', class_='text-break').get_text(strip=True) if address_div else 'N/A'
    phone = address_div.find('a', class_='text-nowrap').get_text(strip=True) if address_div else 'N/A'
    website_div = soup.find('div', string='Website')
    website = website_div.find_next('a')['href'] if website_div else 'N/A'
    return address, phone, website

# Save data
def save_results(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = input("Enter the base name for output files (without extension): ")
    csv_file = f'{output_name}.csv'
    xlsx_file = f'{output_name}.xlsx'

    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        df.to_excel(xlsx_file, index=False)
        logging.info(f"Data saved to {csv_file} and {xlsx_file}")
    except Exception as e:
        logging.error(f"Error saving data: {e}")

# Main process
def main():
    logging.info("Starting scraper...")
    input_file = input("Enter the CSV file name (e.g., wanderlog_restaurants.csv): ")
    restaurants = load_restaurant_links(input_file)
    detailed_data = []

    for index, row in restaurants.iterrows():
        logging.info(f"Scraping {index + 1}/{len(restaurants)}: {row['Link']}")
        if row['Link'] not in [d['Link'] for d in detailed_data]:  # Avoid duplicate scraping
            data = scrape_restaurant_page(row['Link'])
            if data:
                detailed_data.append(data)
            # Add a random delay between 1 and 3 seconds
            time.sleep(random.uniform(1, 3))

    save_results(detailed_data)
    logging.info("Scraper finished successfully.")

if __name__ == "__main__":
    main()
