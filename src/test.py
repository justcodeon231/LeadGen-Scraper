import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def parse_ratings(soup):
    ratings_div = soup.find('div', class_='d-flex flex-wrap')
    return ratings_div.find('span', class_='font-weight-bold').text.strip() if ratings_div else 'N/A'

def parse_contact_info(soup):
    address_div = soup.find('div', class_='col p-0 minw-0')
    if address_div:
        address = address_div.contents[0].strip() if address_div.contents else 'N/A'
        website = address_div.find('a', href=True)['href'] if address_div.find('a', href=True) else 'N/A'
        phone_number = address_div.find('a', href=lambda href: href and 'tel:' in href).text.strip() if address_div.find('a', href=lambda href: href and 'tel:' in href) else 'N/A'
    else:
        address = website = phone_number = 'N/A'
    return address, website, phone_number

def main():
    url = 'https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london'
    page_content = fetch_page_content(url)
    if not page_content:
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    ratings = parse_ratings(soup)
    address, website, phone_number = parse_contact_info(soup)

    print(f'Ratings: {ratings}')
    print(f'Address: {address}')
    print(f'Website: {website}')
    print(f'Phone Number: {phone_number}')

if __name__ == '__main__':
    main()
