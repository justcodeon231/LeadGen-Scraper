import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load CSV file containing restaurant links
csv_file = 'wanderlog_restaurants.csv'  # Replace with your CSV file path
restaurants = pd.read_csv(csv_file)

# Initialize list for storing detailed data
detailed_data = []

# Function to scrape individual restaurant pages
def scrape_restaurant_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Google Ratings
        google_rating_div = soup.find('div', class_='d-flex flex-wrap align-items-center')
        google_stars = google_rating_div.find('span', class_='font-weight-bold').text.strip() if google_rating_div else 'N/A'
        google_how_many = (
            google_rating_div.find('span', class_='ml-1 text-muted').text.strip('()') 
            if google_rating_div and google_rating_div.find('span', class_='ml-1 text-muted') 
            else 'N/A'
        )
        
        # Extract TripAdvisor Ratings
        tripadvisor_rating_div = soup.find_all('div', class_='d-flex flex-wrap align-items-center')[1]  # Assuming TripAdvisor follows Google
        tripadvisor_stars = tripadvisor_rating_div.find('span', class_='font-weight-bold').text.strip() if tripadvisor_rating_div else 'N/A'
        tripadvisor_how_many = (
            tripadvisor_rating_div.find('span', class_='ml-1 text-muted').text.strip('()') 
            if tripadvisor_rating_div and tripadvisor_rating_div.find('span', class_='ml-1 text-muted') 
            else 'N/A'
        )
        
        # Extract Wanderlog Blog Ranking
        wanderlog_ranking_div = soup.find('a', class_='text-muted', href=True)
        wanderlog_ranking = wanderlog_ranking_div.find('span', class_='font-weight-bold').text.strip() if wanderlog_ranking_div else 'N/A'
        wanderlog_list_title = wanderlog_ranking_div.text.replace(wanderlog_ranking, '').strip() if wanderlog_ranking_div else 'N/A'

        # Example data extraction for additional info
        name = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'  # Restaurant name
        address = soup.find('div', class_='address-class').text.strip() if soup.find('div', class_='address-class') else 'N/A'
        phone = soup.find('a', href=lambda href: href and 'tel:' in href).text.strip() if soup.find('a', href=lambda href: href and 'tel:' in href) else 'N/A'
        description = soup.find('div', class_='description-class').text.strip() if soup.find('div', class_='description-class') else 'N/A'

        # Return extracted data as a dictionary
        return {
            'Name': name,
            'Google Stars': google_stars,
            'Google Ratings Count': google_how_many,
            'TripAdvisor Stars': tripadvisor_stars,
            'TripAdvisor Ratings Count': tripadvisor_how_many,
            'Wanderlog Ranking': wanderlog_ranking,
            'Wanderlog List Title': wanderlog_list_title,
            'Address': address,
            'Phone': phone,
            'Description': description,
            'Link': url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Crawl through each restaurant's link
for index, row in restaurants.iterrows():
    print(f"Scraping {row['Name']}...")
    data = scrape_restaurant_page(row['Link'])
    if data:
        detailed_data.append(data)

# Convert to DataFrame
detailed_df = pd.DataFrame(detailed_data)

# Save the detailed data to a new CSV
output_csv = 'wanderlog_restaurant_details.csv'
detailed_df.to_csv(output_csv, index=False)
print(f"Detailed data saved to {output_csv}")

# Print sample of the detailed data
print(detailed_df.head())
