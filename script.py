import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import threading
import sys
import time
import argparse

# Argument parsing setup
def parse_args():
    parser = argparse.ArgumentParser(description="Crawl Etsy shop items.")
    parser.add_argument("--debug", action="store_true", help="Save debug HTML files for each item.")
    parser.add_argument("--url", type=str, help="Etsy shop URL to crawl. If not provided, the script will prompt for it.")
    return parser.parse_args()

# Function to display spinner animation in terminal
def spinner_animation(run_spinner):
    spinner = ['-', '\\', '|', '/']
    i = 0
    while run_spinner():
        sys.stdout.write(spinner[i] + ' Processing... \r')
        sys.stdout.flush()
        time.sleep(0.2)
        i = (i + 1) % 4

# Function to fetch item details
def get_item_details(url, debug=False):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if debug:
        debug_dir = "debug"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        filename = f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.html"
        filepath = os.path.join(debug_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(str(soup))

    name = soup.find('h1').text.strip()

    price_div = soup.find('div', {'data-buy-box-region': 'price'})
    if price_div:
        price_tag = price_div.find('p')
        price = price_tag.text.strip().replace('Price:', '').strip()
    else:
        price = 'N/A'

    reviews = soup.find('button', {'id': 'same-listing-reviews-tab'})
    if reviews:
        review_span = reviews.find('span')
        review_count = review_span.text.strip() if review_span else 'No reviews'
    else:
        review_count = 'No reviews'

    return name, price, review_count, url

# Main function
def main(args):
    # Set up spinner thread
    run_spinner_flag = True
    run_spinner = lambda: run_spinner_flag  # To control spinner from outside the thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(run_spinner,))
    spinner_thread.daemon = True
    spinner_thread.start()

    # Get URL to crawl
    if args.url:
        url = args.url
    else:
        url = input("Please enter the Etsy shop URL to crawl: ")

    # Get HTML content from URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get shop name
    shop_name = soup.find('h1').text.strip()

    # Get URLs of all items in the shop
    item_urls = [link['href'] for item in soup.find_all('div', {'data-appears-component-name': 'shop_home_listing_grid'}) for link in item.find_all('a') if link.has_attr('href')]

    # Get details of each item
    item_details = [get_item_details(item_url, debug=args.debug) for item_url in item_urls]

    # Create a DataFrame from the item details
    df = pd.DataFrame(item_details, columns=['Name', 'Price', 'Reviews', 'URL'])

    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save DataFrame to CSV file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{shop_name}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)

    # Stop spinner animation
    run_spinner_flag = False
    time.sleep(0.5)
    spinner_thread.join()

    # Return CSV data as string
    return df.to_csv(index=False)

if __name__ == "__main__":
    args = parse_args()
    csv_string = main(args)
    print("Processing complete!")