import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


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
        print_hint(guesses_remaining, guess_quote_author,
                   guess_quote_author_link)

    while play_again.lower() not in ("y", "ye", "yes", "n", "no"):
        play_again = input("Would you like to play again (y/n)? ")

    if play_again.lower() in ("y", "ye", "yes"):
        return start_game(quotes)
    else:
        print("Ohk, Goodbye")


def print_hint(guesses_remaining, guess_quote_author, guess_quote_author_link):
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


quotes = read_quotes("all_quotes_scrapped.csv")
start_game(quotes)
