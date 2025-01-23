import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wanderlog page
url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'

# Send GET request
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all restaurant containers
restaurant_divs = soup.find_all('div', class_='d-flex mb-2 align-items-center')

# Initialize list to store restaurant data
restaurant_data = []

# Loop through each restaurant container to extract data
for div in restaurant_divs:
    # Find the <a> tag with the class `color-gray-900` for restaurant name and link
    a_tag = div.find('a', class_='color-gray-900')
    if a_tag:
        name = a_tag.text.strip()  # Restaurant name
        link = a_tag['href']      # Relative link to details page
        full_link = f'https://wanderlog.com{link}'  # Combine with base URL
        restaurant_data.append({'Name': name, 'Link': full_link})

# Convert to DataFrame
df = pd.DataFrame(restaurant_data)

# Save to CSV && Excel
csv_filename = 'wanderlog_restaurants.csv'
xlsx_filename = 'wanderlog_restaurants.xlsx'
df.to_csv(csv_filename, index=False)
df.to_excel(xlsx_filename, index=False)
print(f"Data saved to {csv_filename} and {xlsx_filename}")

# Print sample data
print(df.head())
