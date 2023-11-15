from requests import get
from bs4 import BeautifulSoup
import csv


def extract_first_book(url):
    # gets the HTML code from the site
    page = get(url)

    if page.status_code == 200:  # if the request was successful
        # parse the HTML content using BS
        soup = BeautifulSoup(page.content, 'html.parser')

        # Information about first book
        product_page_url = url
        universal_product_code = soup.find("th", string="UPC").find_next("td").string.strip()
        book_title = soup.find("h1").string.strip()
        price_including_tax = soup.find("th", string="Price (incl. tax)").find_next("td").string.strip()
        price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next("td").string.strip()
        quantity_available = soup.find("th", string="Availability").find_next("td").string.strip()
        product_description = soup.find("div", id="product_description").find_next("p").string.strip()
        category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
        review_rating = soup.find("p", class_="star-rating")["class"][1]
        image_url = soup.find("img")["src"]

        # print(product_page_url, universal_product_code, title, price_excluding_tax, price_including_tax,
        # quantity_available, product_description)
        # print(category, review_rating, image_url)

        # Writing to a CSV file
        with open("book_information.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["Column_headers", "Information"])
            writer.writerows([
                ["product_page_url:", product_page_url],
                ["universal_product_code:", universal_product_code],
                ["book_title:", book_title],
                ["price_including_tax:", price_including_tax],
                ["price_excluding_tax:", price_excluding_tax],
                ["quantity_available:", quantity_available],
                ["product_description:", product_description],
                ["category:", category],
                ["review_rating:", review_rating],
                ["image_url:", image_url]
            ])
    else:
        print("Failed to gather information from book url")


# url of the first book on the index page
book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
extract_first_book(book_url)
