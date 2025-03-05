import requests as req
import pandas as pd
import mysql.connector
from mysql.connector import Error
from openpyxl.workbook import Workbook

# Google Books API key
API_KEY = "AIzaSyDeeRoYXd1ff3xlnpOylhlT9jK2P4UcBGA"
URL = "https://www.googleapis.com/books/v1/volumes"

# Function to fetch books data
def fetch_books(query, max_results = 1000):
    books = []
    start_index = 0
    while len(books) < max_results:
        params = {"q": query, "maxResults": 40, "startIndex": start_index, "key": API_KEY} # Maximum results per API call
        response = req.get(URL, params = params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                sale_info = item.get("saleInfo", {})
                book = {
                    "book_id": item.get("id"),
                    "search_key": query,
                    "book_title": volume_info.get("title"),
                    "book_subtitle": volume_info.get("subtitle", ""),
                    "book_authors": ", ".join(volume_info.get("authors", [])),
                    "book_description": volume_info.get("description", ""),
                    "industryIdentifiers": str(volume_info.get("industryIdentifiers", [])),
                    "text_readingModes": volume_info.get("readingModes", {}).get("text", False),
                    "image_readingModes": volume_info.get("readingModes", {}).get("image", False),
                    "pageCount": volume_info.get("pageCount", 0),
                    "categories": ", ".join(volume_info.get("categories", [])),
                    "language": volume_info.get("language", ""),
                    "imageLinks": str(volume_info.get("imageLinks", {})),
                    "ratingsCount": volume_info.get("ratingsCount", 0),
                    "averageRating": volume_info.get("averageRating", 0.0),
                    "country": sale_info.get("country", ""),
                    "saleability": sale_info.get("saleability", ""),
                    "isEbook": sale_info.get("isEbook", False),
                    "amount_listPrice": sale_info.get("listPrice", {}).get("amount", 0.0),
                    "currencyCode_listPrice": sale_info.get("listPrice", {}).get("currencyCode", ""),
                    "amount_retailPrice": sale_info.get("retailPrice", {}).get("amount", 0.0),
                    "currencyCode_retailPrice": sale_info.get("retailPrice", {}).get("currencyCode", ""),
                    "buyLink": sale_info.get("buyLink", ""),
                    "year": volume_info.get("publishedDate", "").split("-")[0],
                    "publisher": volume_info.get("publisher", "")
                }
                books.append(book)
            start_index += 40  # Move to the next page of results
        else:
            print(f"Error fetching data: {response.status_code}")
            break
    return pd.DataFrame(books)

# Fetch data for the query "dance"
query = "dance"
books_df = fetch_books(query, max_results = 1000)
print(f"Total books fetched: {len(books_df)}")

#To CSV file
output_file = "dance_books.csv"
books_df.to_csv(output_file, index = False)
print(f"Data exported to {output_file}")


