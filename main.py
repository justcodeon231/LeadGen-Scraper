import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import csv
import pandas as pd
import logging
import time
from datetime import datetime
import random
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Combined functions from all apps

def fetch_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def extract_links(html_content, base_url, selector):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.select(selector):
        href = link.get('href', '').strip()
        text = link.get_text(strip=True)
        if base_url and not urlparse(href).netloc:
            href = urljoin(base_url, href)
        links.append({'text': text, 'href': href})
    return links

def save_to_csv(data, filename):
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
    existing_data = []
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    existing_set = {(row['text'], row['href']) for row in existing_data}
    new_data = [row for row in data if (row['text'], row['href']) not in existing_set]
    if new_data:
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['text', 'href'])
            if not existing_data:
                writer.writeheader()
            writer.writerows(new_data)
        logging.info(f"New results added to {filepath}")
    else:
        logging.info("No new data to add.")

def scrape_website(url, selector, filename):
    page_content = fetch_page(url)
    if page_content:
        links = extract_links(page_content, url, selector)
        save_to_csv(links, filename)
        return links
    return []

def scrape_restaurants(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        restaurant_divs = soup.find_all('div', class_='d-flex mb-2 align-items-center')
        restaurant_data = []
        for div in restaurant_divs:
            a_tag = div.find('a', class_='color-gray-900')
            if a_tag:
                name = a_tag.text.strip()
                link = a_tag['href']
                full_link = f'https://wanderlog.com{link}'
                restaurant_data.append({'Name': name, 'Link': full_link})
        return pd.DataFrame(restaurant_data)
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return pd.DataFrame()

def load_restaurant_links(csv_file):
    try:
        csv_path = os.path.join('output', csv_file)
        restaurants = pd.read_csv(csv_path)
        logging.info(f"Loaded {len(restaurants)} restaurant links from {csv_path}")
        return restaurants
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        raise

def scrape_restaurant_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'N/A'
        google_stars, google_reviews = extract_ratings(soup, 0)
        tripadvisor_stars, tripadvisor_reviews = extract_ratings(soup, 1)
        wanderlog_ranking, wanderlog_list = extract_wanderlog_ranking(soup)
        about_text = extract_about(soup)
        address, phone, website = extract_contact_info(soup)
        return {
            'Name': name,
            'Phone': phone,
            'Website': website,
            'Google Stars': google_stars,
            'Google Reviews': google_reviews,
            'TripAdvisor Stars': tripadvisor_stars,
            'TripAdvisor Reviews': tripadvisor_reviews,
            'Wanderlog Ranking': wanderlog_ranking,
            'Wanderlog List': wanderlog_list,
            'About': about_text,
            'Link': url
        }
    except Exception as e:
        logging.error(f"Failed to scrape {url}: {e}")
        return None

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

def save_results(data, output_dir, base_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f'{base_name}.csv'
    xlsx_file = f'{base_name}.xlsx'
    try:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(output_dir, csv_file), index=False)
        df.to_excel(os.path.join(output_dir, xlsx_file), index=False)
        logging.info(f"Data saved to {csv_file} and {xlsx_file}")
    except Exception as e:
        logging.error(f"Error saving results: {e}")

def configure_api(config_path='config.ini'):
    logging.info("Configuring API...")
    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        api_key = config['GoogleGeminiAPI']['api_key']
        if not api_key or len(api_key) < 20:  # Assuming a valid API key is at least 20 characters long
            raise ValueError("Invalid API key in config file.")
        logging.info("API key loaded from config file.")
    except KeyError:
        api_key = input("Enter your Google Gemini API key: ")
        if not api_key or len(api_key) < 20:
            raise ValueError("Invalid API key entered.")
        logging.info("API key entered manually.")
    genai.configure(api_key=api_key)
    logging.info("API configured successfully.")

def generate_ai_response(prompt):
    logging.info(f"Generating AI response for prompt: {prompt}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    logging.info("AI response generated.")
    return response

def process_excel(file_path, output_path):
    logging.info(f"Loading Excel file from {file_path}...")
    data = pd.read_excel(file_path)
    logging.info("Excel file loaded successfully.")
    data['Email'] = ''
    for idx, row in data.iterrows():
        logging.info(f"Processing row {idx + 1}...")
        name = row['Name']
        phone = row['Phone']
        website = row['Website']
        about = row['About']
        summary_prompt = f"Generate a summary for {name} with the following details: Phone: {phone}, Website: {website}, About: {about}."
        summary = generate_with_retries(summary_prompt)
        data.at[idx, 'Summary'] = summary
        logging.info(f"Summary for {name}: {summary}")
        if website.endswith('.co.za'):
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Include a personalized approach to {name} and ask who is in charge of their webpage ({website}). "
                            f"Make the email engaging and encourage them to inquire about how we can help improve their business.")
        elif 'facebook' in website:
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Propose a solution to improve their online presence and suggest the benefits tailored to their business "
                            f"as described: {about}. Focus on making the email compelling and highlighting specific benefits.")
        else:
            email_prompt = (f"Write an introductory email. Introduce me as Leo from Liistudios, a software agency based in East London. "
                            f"Inquire if they would be interested in improving their online presence and optimizing their website ({website}). "
                            f"Make the email engaging and encourage them to inquire about how we can help improve their business.")
        email = generate_with_retries(email_prompt)
        data.at[idx, 'Email'] = email
        logging.info(f"Email for {name}: {email}")
    data.to_excel(output_path, index=False)
    logging.info(f"Output saved to {output_path}")

def generate_with_retries(prompt, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return generate_ai_response(prompt)
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            retries += 1
            if retries >= max_retries:
                logging.error("Max retries reached. Exiting.")
                raise

# Main function to execute the combined application
def main_combined():
    logging.info("Starting combined application...")
    base_name = input("Please enter the base name for output files: ")
    output_dir = os.path.join('output', base_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Example usage of scrape_website
    target_url = input("Please enter the URL to scrape: ")
    selector = '.row.mt-n2.mx-n1 .col-6.col-sm-4.col-md-4.col-lg-4.col-xl-4.mt-2.px-1 a'
    scrape_website(target_url, selector, f'{base_name}_links.csv')
    
    # Example usage of scrape_restaurants
    default_url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'
    url = input(f"Enter Wanderlog URL (press Enter to use default - {default_url}): ") or default_url
    restaurant_df = scrape_restaurants(url)
    print(restaurant_df.head())
    
    # Save the initial restaurant links to CSV
    output_csv = f'{base_name}_restaurants.csv'
    restaurant_df.to_csv(os.path.join(output_dir, output_csv), index=False)
    
    # Load the saved CSV and scrape each restaurant link
    restaurants = load_restaurant_links(output_csv)
    detailed_data = []
    processed_links = set()
    for index, row in restaurants.iterrows():
        logging.info(f"Scraping {index + 1}/{len(restaurants)}: {row['Link']}")
        if row['Link'] not in processed_links:
            data = scrape_restaurant_page(row['Link'])
            if data:
                detailed_data.append(data)
                processed_links.add(row['Link'])
            time.sleep(random.uniform(1, 3))
    save_results(detailed_data, output_dir, base_name)

    # Example usage of AI response generation
    configure_api()
    input_file = os.path.join(output_dir, f"{base_name}.xlsx")
    output_file = os.path.join(output_dir, f"{base_name}_final.xlsx")
    process_excel(input_file, output_file)
    logging.info("Combined application finished successfully.")

if __name__ == "__main__":
    main_combined()
