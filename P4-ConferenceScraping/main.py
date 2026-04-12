# Author: Daniel Walker, Colby Seeley, Adam Halliday
# Program to scrape general conference

from getpass import getpass
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import db


# This function is specifically because of permissions issues for the database (for Daniel lol).
def database_init():
    raw_data = {
        "db_user": input("Enter Postgres Username (default 'postgres'): "),
        "db_host": input("Enter DB host (default 'localhost'): "),
        "db_port": input("Enter the database port (i.e. 5432 or 5434, defaults to 5432): "),
        "db_name": input("Enter the database name (default IS303): ")
    }
    
    # Checks if the user put data into the input
    clean_data = {k: v for k, v in raw_data.items() if v}
    
    # Require mandatory password
    clean_data["db_password"] = getpass("Password: ")
    return db.DatabaseManager(**clean_data)


def scrape_conference(db):
    # Code to scrape general conference data and store data in PostgreSQL database
    # Send a GET request for the relevant church website for the October 2025 General Conference
    response = requests.get(
        "https://www.churchofjesuschrist.org/study/general-conference/2025/10?lang=eng"
    )
    # Eliminate special character conversion problems with BeautifulSoup by specifying the standardized encoding
    response.encoding = "utf-8"
    # Check to make sure scrape request was successful; print out error message if not successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Grab all <li> tags that are specifically categorized as talks - very nice of the church to categorize these items for us
        talk_items = soup.find_all(
            "li", attrs={"data-content-type": "general-conference-talk"}
        )
        # List to store the talk URLs
        talk_urls = []
        # Loop through the the li objects with the general-conference-talk data-content-type
        for item in talk_items:
            # Find the a tag
            link_tag = item.find("a")
            # Get link and combine with full churchofjesuschrist.org website link
            if link_tag:
                relative_url = link_tag.get("href")
                base_url = "https://www.churchofjesuschrist.org"
                full_url = base_url + relative_url
                # Add full url to list of urls
                talk_urls.append(full_url)
        # Loop through URLs, access relevant information, perform processing, and modify values in a dictionary for conversion to DataFrame and subsequent storage in the database.
        for url in talk_urls:
            Conference_Response = requests.get(url)
            # Once again, prevent issues with non-standard characters
            Conference_Response.encoding = "utf-8"
            # Once again, check to make sure GET request is successful
            if Conference_Response.status_code == 200:
                conference_soup = BeautifulSoup(Conference_Response.text, "html.parser")
                # Extract clean title and temporarily store it
                title_talk_item = conference_soup.find("h1")
                clean_title = title_talk_item.get_text(strip=True).replace("\xa0", " ")
                # Extract speaker name and temporarily store it formatted correctly
                name_talk_item = conference_soup.find(
                    "p", attrs={"class": "author-name"}
                )
                clean_name = name_talk_item.get_text(strip=True)[3:].replace(
                    "\xa0", " "
                )
                # Extract kicker and temporarily store it formatted correctly
                kicker_talk_item = conference_soup.find("p", attrs={"class": "kicker"})
                clean_kicker = kicker_talk_item.get_text(strip=True).replace(
                    "\xa0", " "
                )
                # Extract footer information
                footnotes_section = conference_soup.find(
                    "footer", attrs={"class": "notes"}
                )
                # Verify that footnotes are not empty before continuing further; updates database with records saying "N/A" if they aren't present
                if footnotes_section is not None:
                    # Huge dictionary to add items to; DON'T DELETE THIS; THIS IS NEEDED FOR PROGRAM TO FUNCTION AND WAS RECOMMENDED BY INSTRUCTIONS!!!
                    standard_works_dict = {
                        "Speaker_Name": "",
                        "Talk_Name": "",
                        "Kicker": "",
                        "Matthew": 0,
                        "Mark": 0,
                        "Luke": 0,
                        "John": 0,
                        "Acts": 0,
                        "Romans": 0,
                        "1 Corinthians": 0,
                        "2 Corinthians": 0,
                        "Galatians": 0,
                        "Ephesians": 0,
                        "Philippians": 0,
                        "Colossians": 0,
                        "1 Thessalonians": 0,
                        "2 Thessalonians": 0,
                        "1 Timothy": 0,
                        "2 Timothy": 0,
                        "Titus": 0,
                        "Philemon": 0,
                        "Hebrews": 0,
                        "James": 0,
                        "1 Peter": 0,
                        "2 Peter": 0,
                        "1 John": 0,
                        "2 John": 0,
                        "3 John": 0,
                        "Jude": 0,
                        "Revelation": 0,
                        "Genesis": 0,
                        "Exodus": 0,
                        "Leviticus": 0,
                        "Numbers": 0,
                        "Deuteronomy": 0,
                        "Joshua": 0,
                        "Judges": 0,
                        "Ruth": 0,
                        "1 Samuel": 0,
                        "2 Samuel": 0,
                        "1 Kings": 0,
                        "2 Kings": 0,
                        "1 Chronicles": 0,
                        "2 Chronicles": 0,
                        "Ezra": 0,
                        "Nehemiah": 0,
                        "Esther": 0,
                        "Job": 0,
                        "Psalm": 0,
                        "Proverbs": 0,
                        "Ecclesiastes": 0,
                        "Song of Solomon": 0,
                        "Isaiah": 0,
                        "Jeremiah": 0,
                        "Lamentations": 0,
                        "Ezekiel": 0,
                        "Daniel": 0,
                        "Hosea": 0,
                        "Joel": 0,
                        "Amos": 0,
                        "Obadiah": 0,
                        "Jonah": 0,
                        "Micah": 0,
                        "Nahum": 0,
                        "Habakkuk": 0,
                        "Zephaniah": 0,
                        "Haggai": 0,
                        "Zechariah": 0,
                        "Malachi": 0,
                        "1 Nephi": 0,
                        "2 Nephi": 0,
                        "Jacob": 0,
                        "Enos": 0,
                        "Jarom": 0,
                        "Omni": 0,
                        "Words of Mormon": 0,
                        "Mosiah": 0,
                        "Alma": 0,
                        "Helaman": 0,
                        "3 Nephi": 0,
                        "4 Nephi": 0,
                        "Mormon": 0,
                        "Ether": 0,
                        "Moroni": 0,
                        "Doctrine and Covenants": 0,
                        "Moses": 0,
                        "Abraham": 0,
                        "Joseph Smith—Matthew": 0,
                        "Joseph Smith—History": 0,
                        "Articles of Faith": 0,
                    }
                    # Loops through dictionary and assigns relevant values; eliminates non-standard characters
                    footnotes_text = footnotes_section.get_text(strip=True).replace(
                        "\xa0", " "
                    )
                    # Replace dictionary values with count
                    for dict_item in standard_works_dict:
                        scripture_count = footnotes_text.count(dict_item)
                        standard_works_dict[dict_item] = scripture_count
                    # Update dictionary with name, title, kicker
                    standard_works_dict["Speaker_Name"] = clean_name
                    standard_works_dict["Talk_Name"] = clean_title
                    standard_works_dict["Kicker"] = clean_kicker
                    # Transform to pandas dataframe and store in in a table called 'general_conference' in the is303 PostgreSQL database
                    df = pd.DataFrame([standard_works_dict])
                    db.insert_data(df)
                else:
                    # Assigns NaN values along with the title, name, and kicker when footnotes aren't present
                    standard_works_dict = {
                        "Speaker_Name": clean_name,
                        "Talk_Name": clean_title,
                        "Kicker": clean_kicker,
                        "Matthew": float('nan'),
                        "Mark": float('nan'),
                        "Luke": float('nan'),
                        "John": float('nan'),
                        "Acts": float('nan'),
                        "Romans": float('nan'),
                        "1 Corinthians": float('nan'),
                        "2 Corinthians": float('nan'),
                        "Galatians": float('nan'),
                        "Ephesians": float('nan'),
                        "Philippians": float('nan'),
                        "Colossians": float('nan'),
                        "1 Thessalonians": float('nan'),
                        "2 Thessalonians": float('nan'),
                        "1 Timothy": float('nan'),
                        "2 Timothy": float('nan'),
                        "Titus": float('nan'),
                        "Philemon": float('nan'),
                        "Hebrews": float('nan'),
                        "James": float('nan'),
                        "1 Peter": float('nan'),
                        "2 Peter": float('nan'),
                        "1 John": float('nan'),
                        "2 John": float('nan'),
                        "3 John": float('nan'),
                        "Jude": float('nan'),
                        "Revelation": float('nan'),
                        "Genesis": float('nan'),
                        "Exodus": float('nan'),
                        "Leviticus": float('nan'),
                        "Numbers": float('nan'),
                        "Deuteronomy": float('nan'),
                        "Joshua": float('nan'),
                        "Judges": float('nan'),
                        "Ruth": float('nan'),
                        "1 Samuel": float('nan'),
                        "2 Samuel": float('nan'),
                        "1 Kings": float('nan'),
                        "2 Kings": float('nan'),
                        "1 Chronicles": float('nan'),
                        "2 Chronicles": float('nan'),
                        "Ezra": float('nan'),
                        "Nehemiah": float('nan'),
                        "Esther": float('nan'),
                        "Job": float('nan'),
                        "Psalm": float('nan'),
                        "Proverbs": float('nan'),
                        "Ecclesiastes": float('nan'),
                        "Song of Solomon": float('nan'),
                        "Isaiah": float('nan'),
                        "Jeremiah": float('nan'),
                        "Lamentations": float('nan'),
                        "Ezekiel": float('nan'),
                        "Daniel": float('nan'),
                        "Hosea": float('nan'),
                        "Joel": float('nan'),
                        "Amos": float('nan'),
                        "Obadiah": float('nan'),
                        "Jonah": float('nan'),
                        "Micah": float('nan'),
                        "Nahum": float('nan'),
                        "Habakkuk": float('nan'),
                        "Zephaniah": float('nan'),
                        "Haggai": float('nan'),
                        "Zechariah": float('nan'),
                        "Malachi": float('nan'),
                        "1 Nephi": float('nan'),
                        "2 Nephi": float('nan'),
                        "Jacob": float('nan'),
                        "Enos": float('nan'),
                        "Jarom": float('nan'),
                        "Omni": float('nan'),
                        "Words of Mormon": float('nan'),
                        "Mosiah": float('nan'),
                        "Alma": float('nan'),
                        "Helaman": float('nan'),
                        "3 Nephi": float('nan'),
                        "4 Nephi": float('nan'),
                        "Mormon": float('nan'),
                        "Ether": float('nan'),
                        "Moroni": float('nan'),
                        "Doctrine and Covenants": float('nan'),
                        "Moses": float('nan'),
                        "Abraham": float('nan'),
                        "Joseph Smith—Matthew": float('nan'),
                        "Joseph Smith—History": float('nan'),
                        "Articles of Faith": float('nan'),
                    }
                    # Convert to dataframe and store in PostgreSQL database
                    df = pd.DataFrame([standard_works_dict])
                    db.insert_data(df)
            else:
                # Error code if GET request is unsuccessful
                print(
                    f"Failed to retrieve the page. Status code: {Conference_Response.status_code}"
                )
        # Message to indicate that scraping/storage process is complete
        print("\nYou've saved the scraped data to your postgres database.")
    else:
        # Error code if GET request is unsuccessful
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# View summaries of the data
def view_data(db):
    while True:
        iUserChoice = input(
            "\nYou selected to see summaries. Enter 1 to see a summary of all talks. Enter 2 to select a specific talk. Enter anything else to exit: "
        )
        if iUserChoice == "1":
            # Code to see summary of all talks
            db.get_all_talks()
        elif iUserChoice == "2":
            # Code to select a specific talk
           db.get_talk_by_id()
        else:
            #confirm user wants to exit
            s_confirm = input("Are you sure you want to exit? (Y/N) ").strip().lower()
            if s_confirm.startswith('y'):
                end_program()
            else:
                print("Returning to selection menu.")


def end_program():
    print("Closing the program.")
    exit()


if __name__ == "__main__":
    oDatabase = database_init()
    bMainLoop = True
    while bMainLoop:
        print("\n" * 2)
        print("=" * 50)
        print("Welcome to the General Conference Scraper!")
        iUserChoice = input(
            "If you want to scrape data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: "
        )
        if iUserChoice == "1":
            # Perform the scraping process for general conference; passes the Database as a parameter for storage
            scrape_conference(oDatabase)
            # To save to the database, call oDatabase.insert_data(dataframe). Use this to save one row at a time please :)
        elif iUserChoice == "2":
            #take user input and print summary or individual graphs
            view_data(oDatabase)
        else:
            #confirm user wants to exit
            s_confirm = input("Are you sure you want to exit? (Y/N) ").strip().lower()
            if s_confirm.startswith('y'):
                end_program()
            else:
                print("Returning to selection menu.")
