import requests
from bs4 import BeautifulSoup
from csv import writer
from random import choice
from csv import DictWriter

BASE_URL = "http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes_scrapped = []
    page_url = "/page/1"
    while page_url:
        res = requests.get(f"{BASE_URL}{page_url}")
        soup = BeautifulSoup(res.text, "html.parser")
        all_quotes = soup.find_all(attrs={"class": "quote"})

        for quote in all_quotes:
            quote_author = quote.find(attrs={"class": "author"}).get_text()
            quote_content = quote.find(attrs={"class": "text"}).get_text()
            quote_author_slug = quote.find("a")["href"]
            quote_author_link = f"{BASE_URL}{quote_author_slug}"

            all_quotes_scrapped.append({
                "quote_author": quote_author,
                "quote_content": quote_content,
                "quote_author_link": quote_author_link,
            })

        next_button = soup.find(attrs={"class": "next"})
        page_url = next_button.find("a")["href"] if next_button else None
    return all_quotes_scrapped


def write_quotes(quotes):
    with open("all_quotes_scrapped.csv", "w") as csv_file:
        headers = ["quote_author", "quote_content", "quote_author_link"]
        csv_writer = DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()

        for quote in quotes:
            csv_writer.writerow(quote)

        print("All quotes has been successfully scrapped")


quotes = scrape_quotes()
write_quotes(quotes)
