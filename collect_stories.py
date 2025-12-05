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

def download_blue_fairy_book():
    """Download The Blue Fairy Book by Andrew Lang."""
    return download_gutenberg_book(503, "Blue_Fairy_Book")

def download_red_fairy_book():
    """Download The Red Fairy Book by Andrew Lang."""
    return download_gutenberg_book(733, "Red_Fairy_Book")

def download_green_fairy_book():
    """Download The Green Fairy Book by Andrew Lang."""
    return download_gutenberg_book(1349, "Green_Fairy_Book")

def download_greek_myths():
    """Download The Age of Fable by Thomas Bulfinch."""
    return download_gutenberg_book(3326, "Age_of_Fable")

def download_japanese_fairy_tales():
    """Download Japanese Fairy Tales by Yei Theodora Ozaki."""
    return download_gutenberg_book(4018, "Japanese_Fairy_Tales")

def download_russian_fairy_tales():
    """Download Russian Fairy Tales by R. Nisbet Bain."""
    return download_gutenberg_book(22373, "Russian_Fairy_Tales")

def download_wonder_book():
    """Download A Wonder Book by Nathaniel Hawthorne."""
    return download_gutenberg_book(1948, "Wonder_Book")

def download_tanglewood_tales():
    """Download Tanglewood Tales by Nathaniel Hawthorne."""
    return download_gutenberg_book(1376, "Tanglewood_Tales")

def download_legends_of_charlemagne():
    """Download Legends of Charlemagne by Thomas Bulfinch."""
    return download_gutenberg_book(3201, "Legends_of_Charlemagne")

def download_king_arthur_stories():
    """Download King Arthur Stories by James Knowles."""
    return download_gutenberg_book(610, "King_Arthur_Stories")

def download_heroes_of_mythology():
    """Download Heroes of Mythology by Charles Kingsley."""
    return download_gutenberg_book(3926, "Heroes_of_Mythology")

def download_english_fairy_tales():
    """Download English Fairy Tales by Joseph Jacobs."""
    return download_gutenberg_book(7439, "English_Fairy_Tales")

def download_more_english_tales():
    """Download More English Fairy Tales by Joseph Jacobs."""
    return download_gutenberg_book(7438, "More_English_Fairy_Tales")

def download_more_celtic_tales():
    """Download More Celtic Fairy Tales by Joseph Jacobs."""
    return download_gutenberg_book(1045, "More_Celtic_Fairy_Tales")

def download_europa_fairy_tales():
    """Download Europa's Fairy Book by Joseph Jacobs."""
    return download_gutenberg_book(1046, "Europa_Fairy_Tales")

def download_philippine_folk_tales():
    """Download Philippine Folk Tales by Mabel Cook Cole."""
    return download_gutenberg_book(12814, "Philippine_Folk_Tales")

def download_african_stories():
    """Download Folk Stories from Southern Nigeria."""
    return download_gutenberg_book(7213, "African_Stories")

def download_mythology_legends():
    """Download Myths and Legends of All Nations by Logan Marshall."""
    return download_gutenberg_book(11592, "Mythology_Legends")

def download_unicorn_tales():
    """Download The Book of the Thousand Nights and a Night (Arabian Nights continuation)."""
    return download_gutenberg_book(3435, "Unicorn_Tales")

def download_childrens_hour():
    """Download The Children's Hour by Various."""
    return download_gutenberg_book(2785, "Childrens_Hour")

def download_legends_of_king_arthur():
    """Download Legends of King Arthur by Various."""
    return download_gutenberg_book(12753, "Legends_King_Arthur")

def download_mythology_stories():
    """Download Stories from Mythology by Various."""
    return download_gutenberg_book(2786, "Mythology_Stories")

def download_arabian_nights_vol2():
    """Download Arabian Nights Volume 2 (different edition)."""
    return download_gutenberg_book(129, "Arabian_Nights_Vol2")

def download_panchatantra():
    """Download The Panchatantra (Indian fables)."""
    return download_gutenberg_book(2331, "Panchatantra")

def download_hitopadesha():
    """Download The Hitopadesha (Indian fables)."""
    return download_gutenberg_book(2509, "Hitopadesha")

def download_arabian_nights_vol2():
    """Download Arabian Nights Volume 2."""
    return download_gutenberg_book(128, "Arabian_Nights_Vol2")

def download_old_peter_russian_tales():
    """Download Old Peter's Russian Tales by Arthur Ransome."""
    return download_gutenberg_book(22373, "Old_Peter_Russian_Tales")

def download_irish_fairy_tales():
    """Download Irish Fairy Tales by James Stephens."""
    return download_gutenberg_book(2892, "Irish_Fairy_Tales")

def download_welsh_fairy_tales():
    """Download Welsh Fairy Tales by William Elliot Griffis."""
    return download_gutenberg_book(14230, "Welsh_Fairy_Tales")

def download_scandinavian_tales():
    """Download Scandinavian Stories by Various."""
    return download_gutenberg_book(33027, "Scandinavian_Tales")

def download_celtic_fairy_tales():
    """Download Celtic Fairy Tales by Joseph Jacobs."""
    return download_gutenberg_book(1044, "Celtic_Fairy_Tales")

def download_indian_fairy_tales():
    """Download Indian Fairy Tales by Joseph Jacobs."""
    return download_gutenberg_book(7127, "Indian_Fairy_Tales")

def download_household_tales():
    """Download Household Tales by Brothers Grimm (different edition)."""
    return download_gutenberg_book(5314, "Household_Tales")

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
        ("The Blue Fairy Book", download_blue_fairy_book),
        ("The Red Fairy Book", download_red_fairy_book),
        ("The Green Fairy Book", download_green_fairy_book),
        ("The Children's Hour", download_childrens_hour),
        ("Legends of King Arthur", download_legends_of_king_arthur),
        ("Stories from Mythology", download_mythology_stories),
        ("Arabian Nights Volume 2", download_arabian_nights_vol2),
        ("The Age of Fable", download_greek_myths),
        ("Japanese Fairy Tales", download_japanese_fairy_tales),
        ("Russian Fairy Tales", download_russian_fairy_tales),
        ("A Wonder Book", download_wonder_book),
        ("Tanglewood Tales", download_tanglewood_tales),
        ("Legends of Charlemagne", download_legends_of_charlemagne),
        ("King Arthur Stories", download_king_arthur_stories),
        ("Heroes of Mythology", download_heroes_of_mythology),
        ("English Fairy Tales", download_english_fairy_tales),
        ("More English Fairy Tales", download_more_english_tales),
        ("Celtic Fairy Tales", download_celtic_fairy_tales),
        ("More Celtic Fairy Tales", download_more_celtic_tales),
        ("Europa's Fairy Book", download_europa_fairy_tales),
        ("Indian Fairy Tales", download_indian_fairy_tales),
        ("Household Tales", download_household_tales),
        ("Philippine Folk Tales", download_philippine_folk_tales),
        ("Myths and Legends of All Nations", download_mythology_legends),
        ("The Book of the Thousand Nights", download_unicorn_tales),
        ("The Panchatantra", download_panchatantra),
        ("The Hitopadesha", download_hitopadesha),
        ("Old Peter's Russian Tales", download_old_peter_russian_tales),
        ("Irish Fairy Tales", download_irish_fairy_tales),
        ("Welsh Fairy Tales", download_welsh_fairy_tales),
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

