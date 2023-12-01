# OC-P2-PriceMonitoringSystem
This is a beta version of a price monitoring application that tracks book prices for an online book retailer, Books to Scrape. This Python script scrapes book information from Books.toscrape.com and generates CSV files containing book details for each category and an book_images folder containing all of the book images.

## Prerequisites
- Python 3 installed
- Required Python packages include: 'requests', and 'beautifulsoup4'

## Setup
1. Clone this repository using:
   - "https://github.com/julioherrera24/OC-P2-PriceMonitoringSystem.git" inside your local             terminal
   - cd OC-P2-PriceMonitoringSystem
  
2. Install the required packages using pip:
   - "pip install -r requirements.txt"
  

## Usage
1. Run the script "index.py" to scrape all of the book information from books.toscrape.com.
   - python index.py

     This script will extract all of the book information for the different categories from            "https://books.toscrape.com/index.html".

     After the script is successfully executed, you will find CSV files generated for each             category in the project directory that contains all of the book information from their            respective category.

     Each CSV file contains the following information of each book:
        product_page_url
        universal_product_code
        book_title
        price_including_tax
        price_excluding_tax
        quantity_available
        product_description
        category
        review_rating
        image_url

     You will also find a directory named "book_images" that contains all of the images of each        book, in alphabeticaal order.

