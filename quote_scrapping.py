import requests
from bs4 import BeautifulSoup
from csv import writer

all_quotes_scrapped = []

base_url = "http://quotes.toscrape.com"
page_url = "/page/1"

while page_url:
    res = requests.get(f"{base_url}{page_url}")
    soup = BeautifulSoup(res.text, "html.parser")
    all_quotes = soup.find_all(attrs={"class": "quote"})

    for quote in all_quotes:
        quote_author = quote.find(attrs={"class": "author"}).get_text()
        quote_content = quote.find(attrs={"class": "text"}).get_text()
        quote_author_slug = quote.find("a")["href"]
        quote_author_link = f"http://quotes.toscrape.com/{quote_author_slug}"

        all_quotes_scrapped.append({
            "quote_author": quote_author,
            "quote_content": quote_content,
            "quote_author_link": quote_author_link,
        })

    next_button = soup.find(attrs={"class": "next"})
    page_url = next_button.find("a")["href"] if next_button else None

with open("all_quotes_scrapped.csv", "w") as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["quote_author", "quote_content", "quote_author_link"])

    for single_quote_scrapped in all_quotes_scrapped:
        quote_author = single_quote_scrapped["quote_author"]
        quote_content = single_quote_scrapped["quote_content"]
        quote_author_link = single_quote_scrapped["quote_author_link"]
        csv_writer.writerow([quote_author, quote_content, quote_author_link])
