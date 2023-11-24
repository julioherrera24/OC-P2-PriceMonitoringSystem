from requests import get
from bs4 import BeautifulSoup
import csv


def extract_all_categories(url):
    page = get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        all_categories = soup.find("div", class_="side_categories").find_all("a")

        categories = {}
        for category in all_categories:
            category_name = category.text.strip()
            category_url = url.rsplit("/", 1)[0] + "/" + category.get("href")
            categories[category_name] = category_url
        return categories
    else:
        print("Could not retrieve the url page")
        return None

def extract_book_url_on_page(url):  # this function returns all of the book url on a category page
    page = get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        # finds all the books on the page url
        all_books = soup.find_all("article", class_="product_pod")
        book_info = []  # list that will store all the extracted book URLs

        # iterates through every book in the page
        for book in all_books:
            # finds the URL of the book
            book_url = book.find("h3").find("a")["href"]
            # create an absolute URL for each book by combining the argument URL with the book_url variable
            absolute_book_url = url.rsplit("/", 1)[0] + "/" + book_url
            book_info.append(absolute_book_url)  # adds the url to the list

        return book_info  # returns the list of book URLs in the page
    else:  # if page could not be loaded, print an error message
        print("Could not retrieve the url page")
        return None


# this function returns a list of all the books url in a category; in all pages
def books_url_category(category_url):
    page = get(category_url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        number_of_pages = soup.find("li", class_="current").get_text(strip=True)  # find the num of pages
        total_pages = int(number_of_pages.split()[-1])  # max number of pages
        page_number = 1  # use this to iterate through all page numbers
        all_books_url = []  # list that will hold all urls of books

        while page_number <= total_pages:
            # start at the first page of a category
            if page_number == 1:
                page_url = category_url
            else:
                split = category_url.rsplit("/", 1)[0]
                page_url = f'{split}/page-{page_number}.html'

            # returns the list of book url in page url variable
            books_url_on_page = extract_book_url_on_page(page_url)
            # if there are no more books in a page/the page is empty, exit loop
            if not books_url_on_page:
                break
            # add books_url_on_page to the all_books_url list
            all_books_url.extend(books_url_on_page)
            page_number += 1  # move to the next page and continue loop

        return all_books_url  # return the list with all the books url in that category
    else:
        print("Could not retrieve Category url")


# this function extracts all the information in a single book
def extract_book_information(url):
    page = get(url)  # gets the HTML code from the site

    if page.status_code == 200:  # if the request was successful
        # parse the HTML content using BS
        soup = BeautifulSoup(page.content, 'html.parser')

        # gather the information about first book
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

        # create a dictionary with the extracted information
        book_information = {
            "product_page_url": product_page_url,
            "universal_product_code": universal_product_code,
            "book_title": book_title,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "quantity_available": quantity_available,
            "product_description": product_description,
            "category": category,
            "review_rating": review_rating,
            "image_url": image_url
        }
        print("Successfully gathered information and written to 'book_information.csv'")
        return book_information
    else:
        print("Failed to gather information from book url")
        return None


def main():
    category_url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    books_in_category = books_url_category(category_url)

    column_headers = [
        "product_page_url",
        "universal_product_code",
        "book_title",
        "price_including_tax",
        "price_excluding_tax",
        "quantity_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]

    # Writing to a CSV file using a dictionary
    with open("book_information.csv", "w", newline="") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=column_headers)
        writer.writeheader()

        for book_url in books_in_category:
            book_data = extract_book_information(book_url)
            if book_data is not None:
                writer.writerow(book_data)


if __name__ == "__main__":
    main()
