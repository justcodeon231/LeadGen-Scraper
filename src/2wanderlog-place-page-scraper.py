import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('scraper_debug.log'),
        logging.StreamHandler()
    ]
)

# Load CSV file containing restaurant links
logging.info("Starting script execution")
csv_file = 'wanderlog_restaurants.csv'
logging.info(f"Attempting to load CSV file: {csv_file}")

try:
    restaurants = pd.read_csv(csv_file)
    logging.info(f"Successfully loaded CSV with {len(restaurants)} restaurants")
except Exception as e:
    logging.error(f"Failed to load CSV file: {e}")
    raise

# Initialize list for storing detailed data
detailed_data = []

def scrape_restaurant_page(url, index):
    logging.info(f"\n{'='*50}")
    logging.info(f"Processing restaurant #{index+1}")
    logging.info(f"URL: {url}")
    start_time = time.time()

    try:
        logging.info("Sending HTTP request...")
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Response received. Status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.info("HTML parsed successfully")

        # Extract Google Ratings
        logging.info("Extracting Google ratings...")
        google_rating_div = soup.find('div', class_='d-flex flex-wrap align-items-center')
        google_stars = google_rating_div.find('span', class_='font-weight-bold').text.strip() if google_rating_div else 'N/A'
        google_how_many = (
            google_rating_div.find('span', class_='ml-1 text-muted').text.strip('()') 
            if google_rating_div and google_rating_div.find('span', class_='ml-1 text-muted') 
            else 'N/A'
        )
        logging.info(f"Google ratings found - Stars: {google_stars}, Count: {google_how_many}")

        # Extract TripAdvisor Ratings
        logging.info("Extracting TripAdvisor ratings...")
        tripadvisor_rating_div = soup.find_all('div', class_='d-flex flex-wrap align-items-center')[1] if len(soup.find_all('div', class_='d-flex flex-wrap align-items-center')) > 1 else None
        tripadvisor_stars = tripadvisor_rating_div.find('span', class_='font-weight-bold').text.strip() if tripadvisor_rating_div else 'N/A'
        tripadvisor_how_many = (
            tripadvisor_rating_div.find('span', class_='ml-1 text-muted').text.strip('()') 
            if tripadvisor_rating_div and tripadvisor_rating_div.find('span', class_='ml-1 text-muted') 
            else 'N/A'
        )
        logging.info(f"TripAdvisor ratings found - Stars: {tripadvisor_stars}, Count: {tripadvisor_how_many}")

        # Extract Wanderlog Blog Ranking
        logging.info("Extracting Wanderlog ranking...")
        wanderlog_ranking_div = soup.find('div', class_='d-flex flex-row align-items-center flex-wrap')
        wanderlog_ranking_tag = wanderlog_ranking_div.find('a', class_='text-muted') if wanderlog_ranking_div else None
        wanderlog_ranking = 'N/A'
        wanderlog_list_title = 'N/A'
        if wanderlog_ranking_tag:
            wanderlog_ranking = wanderlog_ranking_tag.find('span', class_='font-weight-bold').text.strip() if wanderlog_ranking_tag.find('span', class_='font-weight-bold') else 'N/A'
            wanderlog_list_title = wanderlog_ranking_tag.text.replace(wanderlog_ranking, '').strip() if wanderlog_ranking else 'N/A'
        logging.info(f"Wanderlog ranking found - Rank: {wanderlog_ranking}, List: {wanderlog_list_title}")

        # Extract other information
        logging.info("Extracting additional information...")
        
        name = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
        logging.info(f"Name found: {name}")

        # Extract About text based on provided HTML structure
        logging.info("Extracting About text...")
        main_div = soup.find('div', class_='col col-md-8')  # Find the main container
        if main_div:
            next_div = main_div.find_next('div', class_='mt-5')  # Find the next div with class 'mt-5'
            if next_div:
                about_section = next_div.find('h2', class_='font-weight-bold mb-3 line-height-1 color-primary-darkest')  # Find the h2
                if about_section:
                    about_text = about_section.find_next('div')  # Find the div after the h2
                    about_text = about_text.get_text(strip=True) if about_text else 'N/A'  # Get the text inside the div
                else:
                    about_text = 'N/A'
            else:
                about_text = 'N/A'
        else:
            about_text = 'N/A'
        logging.info(f"About text found: {about_text[:50]}...")

        # Extract Address from the div with class "mt-3" and "text-break"
        logging.info("Extracting address...")
        address_div = soup.find('div', class_='mt-3')
        address = 'N/A'
        if address_div:
            address_tag = address_div.find('a', class_='text-break')  # Look for "text-break" class
            if address_tag:
                address = address_tag.text.strip()  # Extract address text from <a> tag
                logging.info(f"Address found: {address}")

        # Extract Phone number from the div with class "mt-3" and "text-nowrap"
        logging.info("Extracting phone number...")
        phone = 'N/A'
        phone_div = soup.find('div', class_='mt-3')
        if phone_div:
            phone_tag = phone_div.find('a', class_='text-nowrap')  # Look for "text-nowrap" class
            if phone_tag:
                phone = phone_tag.text.strip()  # Extract phone number text from <a> tag
                logging.info(f"Phone found: {phone}")

        website_div = soup.find('div', text='Website')
        website = website_div.find_next('a')['href'] if website_div else 'N/A'
        logging.info(f"Website found: {website}")

        description = "N/A"

        # Calculate scraping time
        end_time = time.time()
        logging.info(f"Page scraped in {end_time - start_time:.2f} seconds")

        return {
            'Name': name,
            'Google Stars': google_stars,
            'Google Ratings Count': google_how_many,
            'TripAdvisor Stars': tripadvisor_stars,
            'TripAdvisor Ratings Count': tripadvisor_how_many,
            'Wanderlog Ranking': wanderlog_ranking,
            'Wanderlog List Title': wanderlog_list_title,
            'About': about_text,
            'Address': address,
            'Phone': phone,
            'Website': website,
            'Description': description,
            'Link': url
        }

    except Exception as e:
        logging.error(f"Error scraping {url}")
        logging.error(f"Error details: {str(e)}")
        logging.error("Stack trace:", exc_info=True)
        return None

# Main scraping loop
logging.info(f"\nStarting main scraping loop for {len(restaurants)} restaurants")
start_time_total = time.time()

# Initialize detailed_data with any existing data if file exists
try:
    existing_df = pd.read_csv('wanderlog_restaurant_details_latest.csv')
    detailed_data = existing_df.to_dict('records')
    logging.info(f"Loaded {len(detailed_data)} existing records")
except FileNotFoundError:
    detailed_data = []
    logging.info("No existing data found, starting fresh")

for index, row in restaurants.iterrows():
    logging.info(f"\nProcessing restaurant {index+1} of {len(restaurants)}")
    
    # Check if URL already exists
    existing_entry = next((item for item in detailed_data if item['Link'] == row['Link']), None)
    
    data = scrape_restaurant_page(row['Link'], index)
    if data:
        if existing_entry:
            # Update only empty or N/A values
            for key, value in data.items():
                if existing_entry[key] in ['N/A', '', None] and value not in ['N/A', '', None]:
                    existing_entry[key] = value
                    logging.info(f"Updated {key} for {data['Name']}")
        else:
            detailed_data.append(data)
            logging.info(f"Added new entry for: {data['Name']}")
    else:
        logging.warning(f"Failed to scrape restaurant at index {index}")

# Save latest version for future reference
pd.DataFrame(detailed_data).to_csv('wanderlog_restaurant_details_latest.csv', index=False)

# Calculate total execution time
end_time_total = time.time()
total_time = end_time_total - start_time_total
logging.info(f"\nTotal execution time: {total_time:.2f} seconds")
logging.info(f"Average time per restaurant: {total_time/len(restaurants):.2f} seconds")

# Save results
logging.info("\nPreparing to save results...")
detailed_df = pd.DataFrame(detailed_data)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_csv = f'wanderlog_restaurant_details_{timestamp}.csv'
output_xlsx = f'wanderlog_restaurant_details_{timestamp}.xlsx'

try:
    # Save as CSV
    detailed_df.to_csv(output_csv, index=False)
    logging.info(f"Successfully saved data to {output_csv}")
    
    # Save as XLSX
    detailed_df.to_excel(output_xlsx, index=False)
    logging.info(f"Successfully saved data to {output_xlsx}")
    
    logging.info(f"Total restaurants scraped: {len(detailed_data)} out of {len(restaurants)}")
    logging.info(f"Success rate: {(len(detailed_data)/len(restaurants))*100:.2f}%")
except Exception as e:
    logging.error(f"Error saving files: {e}")

# Print sample of the detailed data
logging.info("\nSample of scraped data:")
logging.info(detailed_df.head().to_string())
