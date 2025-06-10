import requests
import os
import random
import time
import argparse

def download_gutenberg_book(gutenberg_id, output_file="gutenberg.txt"):
    """
    Downloads a single book from Project Gutenberg given its ID.
    Attempts to download the plain text UTF-8 version.
    """
    # Try the most common format first
    url_base = f"https://www.gutenberg.org/files/{gutenberg_id}"
    possible_urls = [
        f"{url_base}/{gutenberg_id}.txt",
        f"{url_base}/{gutenberg_id}-0.txt",
        f"{url_base}/{gutenberg_id}-8.txt", # Sometimes older formats might be -8
    ]

    for url in possible_urls:
        try:
            print(f"Attempting to download: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            with open(output_file, 'a') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded Project Gutenberg ID {gutenberg_id} to {output_file}")
            return output_file
        except requests.exceptions.RequestException as e:
            print(f"Could not download from {url}: {e}")
            continue # Try next URL

    print(f"Failed to download Project Gutenberg ID {gutenberg_id} using any known URL patterns.")
    return None

def download_subset_of_gutenberg_books(num_books=5, output_file="gutenberg.txt"):
    """
    Downloads a random sample of books from Project Gutenberg.

    Args:
        num_books (int): The number of books to download.
    """
    random_id_range=(1, 70000)
    downloaded_count = 0

    # Generate unique random IDs within the specified range
    # We'll try to get more than needed in case some IDs don't correspond to valid texts
    potential_ids = set()
    while len(potential_ids) < num_books * 2:
        potential_ids.add(random.randint(random_id_range[0], random_id_range[1]))

    for book_id in potential_ids:
        if downloaded_count >= num_books:
            print(f"Reached desired number of {num_books} downloads.")
            break

        print(f"\n--- Processing Project Gutenberg ID: {book_id} ---")
        if download_gutenberg_book(book_id):
            downloaded_count += 1

        # Be polite and add a small delay between requests
        time.sleep(1)

    print(f"\n--- Download Summary ---")
    print(f"Total books requested: {len(potential_ids)}")
    print(f"Total books successfully downloaded: {downloaded_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download books from Project Gutenberg")
    parser.add_argument("--num-books", type=int, default=10, help="Number of books to download")
    parser.add_argument("--output-file", type=str, default="gutenberg.txt", help="Output file name")
    args = parser.parse_args()
    download_subset_of_gutenberg_books(num_books=args.num_books, output_file=args.output_file)
