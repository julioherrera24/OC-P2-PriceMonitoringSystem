from requests import get
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
page = get(url)

soup = BeautifulSoup(page.content, 'html.parser')

