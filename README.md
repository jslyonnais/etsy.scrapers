# Etsy Shop Scraper

This script extracts item details from a specified Etsy shop page and saves them into a CSV file.

## Features:

- Extracts item name, price, number of reviews, and the direct URL to the item from the Etsy shop.
- Option to provide the Etsy shop URL as a command-line argument.
- Debug mode to save the raw HTML content of each item page, useful for inspection or troubleshooting.

## Usage:

1. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

1. Run the script:

   - Without URL argument (will prompt for URL):

     ```bash
     python script.py
     ```

   - With URL argument:

     ```bash
     python script.py --url "https://www.etsy.com/shop/ShopName"
     ```

   - With debug mode (saves raw HTML):
     ```bash
     python script.py --debug
     ```

## Output:

- The extracted details are saved into a CSV file in the "output" directory. The filename is based on the shop's name and includes a timestamp.

## Debug Mode:

If the `--debug` flag is active, the script will save the raw HTML content of each item page to a "debug" folder, aiding in inspection and troubleshooting.
