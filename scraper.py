import requests
from bs4 import BeautifulSoup
import csv

# The website we're scraping (legal practice site)
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

# This list will hold all our results
all_books = []

# We'll scrape the first 5 pages
current_url = START_URL

for page_number in range(1, 6):
    print(f"Scraping page {page_number}...")

    # Fetch the page
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all book listings on the page
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        # Extract the title
        title = book.find("h3").find("a")["title"]

        # Extract the price
        price = book.find("p", class_="price_color").text.strip()

        # Extract the star rating (stored as a word like "Three")
        rating_word = book.find("p", class_="star-rating")["class"][1]

        # Save this book as a dictionary
        all_books.append({
            "title": title,
            "price": price,
            "rating": rating_word
        })

    # Move to the next page
    current_url = f"{BASE_URL}page-{page_number + 1}.html"

# Save everything to a CSV file
with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
    writer.writeheader()
    writer.writerows(all_books)

print(f"Done! Scraped {len(all_books)} books. Saved to books.csv")