import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wanderlog():
    """
    Scrape Wanderlog for restaurant data in East London.
    """
    url = "https://wanderlog.com/list/geoCategory/205480/where-to-eat-best-restaurants-in-east-london"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch data. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    restaurants = []

    # Extract relevant data using the provided selectors
    for item in soup.select(".poi-container"):  
        name = item.select_one(".poi-title").text.strip() if item.select_one(".poi-title") else "N/A"
        website = item.select_one(".poi-website a")['href'] if item.select_one(".poi-website a") else "N/A"
        rating = item.select_one(".poi-rating").text.strip() if item.select_one(".poi-rating") else "N/A"
        description = item.select_one(".poi-description").text.strip() if item.select_one(".poi-description") else "N/A"
        phone = item.select_one(".poi-contact").text.strip() if item.select_one(".poi-contact") else "N/A"

        restaurants.append({
            "Name": name,
            "Website": website,
            "Rating": rating,
            "Description": description,
            "Phone": phone
        })

    return restaurants

def scrape_dining_out():
    """
    Scrape Dining-Out for restaurant data in East London.
    """
    url = "https://www.dining-out.co.za/restaurants/East-London/404"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch data. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    restaurants = []

    # Extract relevant data using the provided selectors
    for item in soup.select(".restaurant-list-item"):  
        name = item.select_one(".restaurant-name a").text.strip() if item.select_one(".restaurant-name a") else "N/A"
        address = item.select_one(".restaurant-address").text.strip() if item.select_one(".restaurant-address") else "N/A"
        phone = item.select_one(".restaurant-contact").text.strip() if item.select_one(".restaurant-contact") else "N/A"
        website = item.select_one(".restaurant-website a")['href'] if item.select_one(".restaurant-website a") else "N/A"
        rating = item.select_one(".restaurant-rating").text.strip() if item.select_one(".restaurant-rating") else "N/A"
        description = item.select_one(".restaurant-description").text.strip() if item.select_one(".restaurant-description") else "N/A"

        restaurants.append({
            "Name": name,
            "Website": website,
            "Rating": rating,
            "Description": description,
            "Phone": phone,
            "Address": address
        })

    return restaurants

def save_to_csv(data, filename):
    """
    Save the scraped data to a CSV file.
    """
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    print("Select the website to scrape:")
    print("1. Wanderlog (East London Restaurants)")
    print("2. Dining-Out (East London Restaurants)")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        print("Scraping Wanderlog...")
        data = scrape_wanderlog()
        filename = "wanderlog_restaurants.csv"
    elif choice == "2":
        print("Scraping Dining-Out...")
        data = scrape_dining_out()
        filename = "dining_out_restaurants.csv"
    else:
        print("Invalid choice. Exiting...")
        return

    if data:
        print(f"Scraped {len(data)} entries. Sample data:")
        for item in data[:5]:  # Show first 5 entries
            print(item)
        save_to_csv(data, filename)
    else:
        print("No data scraped. Please check the website or scraper.")

if __name__ == "__main__":
    main()
