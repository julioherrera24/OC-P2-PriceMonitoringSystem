from requests import get
from bs4 import BeautifulSoup
import csv


def extract_all_categories(url):   # this function will extract all categories available
    page = get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        # scrapes all categories available in the page, including name and url
        all_categories = soup.find("div", class_="side_categories").find_all("a")

        categories = {}   # dictionary that will hold keys = categories, values = url
        for category in all_categories:   # loop through all_categories
            category_name = category.text.strip()   # key = category_name
            category_url = url.rsplit("/", 1)[0] + "/" + category.get("href")  # value is url
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
    else:
        return None


# this function returns a list of all the books url in a category; in all pages
def books_url_category(category_url):
    base_url = category_url   # first page of category
    next_page_url = category_url.rsplit("/", 1)[0]   # variable to use for the next pages
    page_number = 1
    book_links = []    # list to hold all of the book urls in category

    while True:  # iterate until a page does not contain the next button
        current_url = f"{next_page_url}/page-{page_number}.html" if page_number > 1 else base_url
        page = get(current_url)

        if page.status_code == 200:
            # call function to get list of all books in the current page
            book_links_on_page = extract_book_url_on_page(current_url)
            if book_links_on_page:
                # if there are book urls in the list, add them to book_links
                book_links.extend(book_links_on_page)
            else:
                # if there weren't any books, break out of the loop
                break

            soup = BeautifulSoup(page.content, 'html.parser')
            # parse through html code to find if a next button exists
            next_button = soup.find("li", class_="next")
            if next_button is None:
                break  # if there is no next button on page, stop iteration
            else:
                page_number += 1  # proceed to next page to get more book urls
        else:
            break  # stop loop if page doesn't exist
    return book_links


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
    # category_url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    # books_in_category = books_url_category(category_url)

    main_url = "https://books.toscrape.com/index.html"
    all_categories = extract_all_categories(main_url)

    all_books_found = {}
    for name, url in all_categories.items():
        all_books_found[name] = books_url_category(url)

    for k, v in all_books_found.items():
        print(k, len(v))

    '''
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
    '''


if __name__ == "__main__":
    main()
