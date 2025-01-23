import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape restaurant data from the Wanderlog page
def scrape_restaurants(url):
    # Send GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all restaurant containers
    restaurant_divs = soup.find_all('div', class_='d-flex mb-2 align-items-center')

    # Initialize list to store restaurant data
    restaurant_data = []

    # Loop through each restaurant container to extract data
    for div in restaurant_divs:
        a_tag = div.find('a', class_='color-gray-900')
        if a_tag:
            name = a_tag.text.strip()  # Restaurant name
            link = a_tag['href']      # Relative link to details page
            full_link = f'https://wanderlog.com{link}'  # Combine with base URL
            restaurant_data.append({'Name': name, 'Link': full_link})

    # Convert to DataFrame
    return pd.DataFrame(restaurant_data)

# Main function to execute the scraper
def main():
    # URL of the Wanderlog page
    # Ask user for URL or use default
    default_url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'
    url = input(f"Enter Wanderlog URL (press Enter to use default - {default_url}): ") or default_url

    # Scrape restaurant data
    restaurant_df = scrape_restaurants(url)

    # Save to CSV & Excel
    # Ask for custom filename (without extension)
    default_name = 'wanderlog_restaurants'
    base_filename = input(f"Enter filename without extension (press Enter to use default - {default_name}): ") or default_name
    
    # Create filenames with extensions
    csv_filename = f'{base_filename}.csv'
    xlsx_filename = f'{base_filename}.xlsx'
    restaurant_df.to_csv(csv_filename, index=False)
    restaurant_df.to_excel(xlsx_filename, index=False)

    # Print success message and sample data
    print(f"Data saved to {csv_filename} and {xlsx_filename}")
    print("Sample data:")
    print(restaurant_df.head())

if __name__ == "__main__":
    main()
