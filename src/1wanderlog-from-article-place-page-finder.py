import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import csv

# Function to scrape restaurant data from the Wanderlog page
def scrape_restaurants(url):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
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
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return pd.DataFrame()

# Main function to execute the scraper
def main():
    # Ask user for URL or file
    choice = input("Enter '1' to input a URL or '2' to read from a file: ")

    urls = []
    if choice == '1':
        # URL of the Wanderlog page
        default_url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'
        url = input(f"Enter Wanderlog URL (press Enter to use default - {default_url}): ") or default_url
        urls.append(url)
    elif choice == '2':
        # Ask for file path
        file_path = input("Enter the path to the CSV file (e.g., 'urls.csv'): ")
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if len(row) > 1:
                        urls.append(row[1])  # Assuming the second column contains the URLs
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return

    if not urls:
        print("No URLs to scrape.")
        return

    # Initialize DataFrame to store all restaurant data
    all_restaurant_data = pd.DataFrame()

    # Scrape restaurant data for each URL
    for url in urls:
        restaurant_df = scrape_restaurants(url)
        all_restaurant_data = pd.concat([all_restaurant_data, restaurant_df], ignore_index=True)

    if all_restaurant_data.empty:
        print("No data scraped.")
        return

    # Save to CSV & Excel
    # Ask for custom filename (without extension)
    default_name = 'wanderlog_restaurants'
    base_filename = input(f"Enter filename without extension (press Enter to use default - {default_name}): ") or default_name

    # Create output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Create filenames with extensions
    csv_filename = os.path.join(output_dir, f'{base_filename}.csv')
    xlsx_filename = os.path.join(output_dir, f'{base_filename}.xlsx')
    all_restaurant_data.to_csv(csv_filename, index=False)
    all_restaurant_data.to_excel(xlsx_filename, index=False)

    # Print success message and sample data
    print(f"Data saved to {csv_filename} and {xlsx_filename}")
    print("Sample data:")
    print(all_restaurant_data.head())

if __name__ == "__main__":
    main()
