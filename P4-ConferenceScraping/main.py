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
    db_user = input("Enter Postgres Username (usually 'postgres'): ")
    db_password = getpass("Enter Postgres Password: ")
    db_host = "localhost"
    db_port = "5432"
    db_name = "is303"
    oDatabase = db.DatabaseManager(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return oDatabase


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
                # Extract the number of times each book of scripture is listed in the references
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
                    # Assigns "N/A" values along with the title, name, and kicker when footnotes aren't present
                    standard_works_dict = {
                        "Speaker_Name": clean_name,
                        "Talk_Name": clean_title,
                        "Kicker": clean_kicker,
                        "Matthew": "N/A",
                        "Mark": "N/A",
                        "Luke": "N/A",
                        "John": "N/A",
                        "Acts": "N/A",
                        "Romans": "N/A",
                        "1 Corinthians": "N/A",
                        "2 Corinthians": "N/A",
                        "Galatians": "N/A",
                        "Ephesians": "N/A",
                        "Philippians": "N/A",
                        "Colossians": "N/A",
                        "1 Thessalonians": "N/A",
                        "2 Thessalonians": "N/A",
                        "1 Timothy": "N/A",
                        "2 Timothy": "N/A",
                        "Titus": "N/A",
                        "Philemon": "N/A",
                        "Hebrews": "N/A",
                        "James": "N/A",
                        "1 Peter": "N/A",
                        "2 Peter": "N/A",
                        "1 John": "N/A",
                        "2 John": "N/A",
                        "3 John": "N/A",
                        "Jude": "N/A",
                        "Revelation": "N/A",
                        "Genesis": "N/A",
                        "Exodus": "N/A",
                        "Leviticus": "N/A",
                        "Numbers": "N/A",
                        "Deuteronomy": "N/A",
                        "Joshua": "N/A",
                        "Judges": "N/A",
                        "Ruth": "N/A",
                        "1 Samuel": "N/A",
                        "2 Samuel": "N/A",
                        "1 Kings": "N/A",
                        "2 Kings": "N/A",
                        "1 Chronicles": "N/A",
                        "2 Chronicles": "N/A",
                        "Ezra": "N/A",
                        "Nehemiah": "N/A",
                        "Esther": "N/A",
                        "Job": "N/A",
                        "Psalm": "N/A",
                        "Proverbs": "N/A",
                        "Ecclesiastes": "N/A",
                        "Song of Solomon": "N/A",
                        "Isaiah": "N/A",
                        "Jeremiah": "N/A",
                        "Lamentations": "N/A",
                        "Ezekiel": "N/A",
                        "Daniel": "N/A",
                        "Hosea": "N/A",
                        "Joel": "N/A",
                        "Amos": "N/A",
                        "Obadiah": "N/A",
                        "Jonah": "N/A",
                        "Micah": "N/A",
                        "Nahum": "N/A",
                        "Habakkuk": "N/A",
                        "Zephaniah": "N/A",
                        "Haggai": "N/A",
                        "Zechariah": "N/A",
                        "Malachi": "N/A",
                        "1 Nephi": "N/A",
                        "2 Nephi": "N/A",
                        "Jacob": "N/A",
                        "Enos": "N/A",
                        "Jarom": "N/A",
                        "Omni": "N/A",
                        "Words of Mormon": "N/A",
                        "Mosiah": "N/A",
                        "Alma": "N/A",
                        "Helaman": "N/A",
                        "3 Nephi": "N/A",
                        "4 Nephi": "N/A",
                        "Mormon": "N/A",
                        "Ether": "N/A",
                        "Moroni": "N/A",
                        "Doctrine and Covenants": "N/A",
                        "Moses": "N/A",
                        "Abraham": "N/A",
                        "Joseph Smith—Matthew": "N/A",
                        "Joseph Smith—History": "N/A",
                        "Articles of Faith": "N/A",
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
def view_data():
    while True:
        iUserChoice = input(
            "\nYou selected to see summaries. Enter 1 to see a summary of all talks. Enter 2 to select a specific talk. Enter anything else to exit: "
        )
        if iUserChoice == "1":
            # Code to see summary of all talks
            pass
        elif iUserChoice == "2":
            # Code to select a specific talk
            print("\nThe following are the names of speakers and their talks: ")

            print("\nPlease enter the number of the talk you want to see summarized: ")
            while True:
                try:
                    iTalkChoice = int(input())
                    # Code to show summary of selected talk

                except ValueError:
                    print("Invalid input. Please enter a number.")
                except KeyError:
                    print("Invalid talk number. Please enter a valid number.")
        else:
            end_program()


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
            view_data()
        else:
            end_program()
