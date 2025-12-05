"""
Script to collect public domain stories from Project Gutenberg and other sources.
This script downloads story collections and saves them as text files.
"""

import os
import requests
from bs4 import BeautifulSoup
import time

# Create stories directory if it doesn't exist
os.makedirs("stories", exist_ok=True)

def download_gutenberg_book(book_id, title):
    """Download a book from Project Gutenberg by ID."""
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    
    try:
        print(f"Downloading {title}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save to file
        filename = f"stories/{title.replace(' ', '_').replace('/', '_')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ Saved {title} to {filename}")
        return filename
    except Exception as e:
        print(f"✗ Error downloading {title}: {e}")
        return None

def download_aesop_fables():
    """Download Aesop's Fables from Project Gutenberg."""
    return download_gutenberg_book(21, "Aesops_Fables")

def download_grimm_fairy_tales():
    """Download Grimm's Fairy Tales from Project Gutenberg."""
    return download_gutenberg_book(2591, "Grimms_Fairy_Tales")

def download_andersen_fairy_tales():
    """Download Andersen's Fairy Tales from Project Gutenberg."""
    return download_gutenberg_book(1597, "Andersens_Fairy_Tales")

def download_arabian_nights():
    """Download Arabian Nights from Project Gutenberg."""
    return download_gutenberg_book(128, "Arabian_Nights")

def download_just_so_stories():
    """Download Just So Stories by Rudyard Kipling."""
    return download_gutenberg_book(2781, "Just_So_Stories")

def download_jataka_tales():
    """Download Jataka Tales (Buddhist stories) from Project Gutenberg."""
    return download_gutenberg_book(3600, "Jataka_Tales")

def main():
    """Main function to download all story collections."""
    print("=" * 60)
    print("JStory - Story Collection Script")
    print("=" * 60)
    print("\nDownloading public domain story collections...\n")
    
    books = [
        ("Aesop's Fables", download_aesop_fables),
        ("Grimm's Fairy Tales", download_grimm_fairy_tales),
        ("Andersen's Fairy Tales", download_andersen_fairy_tales),
        ("Arabian Nights", download_arabian_nights),
        ("Just So Stories", download_just_so_stories),
        ("Jataka Tales", download_jataka_tales),
    ]
    
    downloaded = []
    for title, download_func in books:
        result = download_func()
        if result:
            downloaded.append((title, result))
        time.sleep(1)  # Be respectful to Project Gutenberg
    
    print("\n" + "=" * 60)
    print(f"Downloaded {len(downloaded)} books:")
    for title, filename in downloaded:
        print(f"  - {title}: {filename}")
    print("=" * 60)

if __name__ == "__main__":
    main()

