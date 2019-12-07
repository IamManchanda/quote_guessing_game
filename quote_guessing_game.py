import requests
from bs4 import BeautifulSoup
from csv import writer
from random import choice

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


def start_game(quotes):
    guess = ""
    guesses_remaining = 4
    play_again = ""
    guess_quote = choice(quotes)
    guess_quote_author = guess_quote["quote_author"]
    guess_quote_author_link = guess_quote["quote_author_link"]
    guess_quote_content = guess_quote["quote_content"]

    print(f"Here is a quote: {guess_quote_content}")
    print(f"Author name: {guess_quote_author}")

    while guess.lower() != guess_quote_author.lower() and guesses_remaining > 0:
        guess = input(
            f"Guesses Remaining: {guesses_remaining}. Who said this Quote? ")

        if guess.lower() == guess_quote_author.lower():
            print("Congrats! You got it right!!!")
            break

        guesses_remaining -= 1

        if guesses_remaining == 3:
            res = requests.get(guess_quote_author_link)
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(
                attrs={"class": "author-born-date"}).get_text()
            birth_place = soup.find(
                attrs={"class": "author-born-location"}).get_text()
            print(
                f"Here is a Hint: The author was born on {birth_date} {birth_place}")
        elif guesses_remaining == 2:
            first_initial = guess_quote_author[0]
            print(
                f"Here is a Hint: The author first name starts with: {first_initial}")
        elif guesses_remaining == 1:
            last_initial = guess_quote_author.split(" ")[-1][0]
            print(
                f"Here is a Hint: The author last name starts with: {last_initial}")
        else:
            print(
                f"Sorry, you ran out of guesses. The answer was {guess_quote_author}")

    while play_again.lower() not in ("y", "ye", "yes", "n", "no"):
        play_again = input("Would you like to play again (y/n)? ")

    if play_again.lower() in ("y", "ye", "yes"):
        return start_game(quotes)
    else:
        print("Ohk, Goodbye")


quotes = scrape_quotes()
start_game(quotes)
