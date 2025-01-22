import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'

# Send a GET request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract Ratings Data
ratings_div = soup.find('div', class_='d-flex flex-wrap')
ratings = ratings_div.find('span', class_='font-weight-bold').text.strip() if ratings_div else 'N/A'

# Extract Website, Address, and Contact Info
address_div = soup.find('div', class_='col p-0 minw-0')
if address_div:
    address = address_div.contents[0].strip() if address_div.contents else 'N/A'
    website = address_div.find('a', href=True)['href'] if address_div.find('a', href=True) else 'N/A'
    phone_number = address_div.find('a', href=lambda href: href and 'tel:' in href).text.strip() if address_div.find('a', href=lambda href: href and 'tel:' in href) else 'N/A'
else:
    address = website = phone_number = 'N/A'

# Extract Place Description (from the mt-2 div)
# place_description_div = soup.find('div', class_='mt-2')
# place_description = place_description_div.get_text(strip=True) if place_description_div else 'N/A'

# Filter out unwanted "map layers" or "overview" text
# if "Map layers" in place_description:
#     place_description = place_description.split("Map layers")[0].strip()

# Print or save the extracted data
print(f'Ratings: {ratings}')
print(f'Address: {address}')
print(f'Website: {website}')
print(f'Phone Number: {phone_number}')
# print(f'Place Description: {place_description}')
