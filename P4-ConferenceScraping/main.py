# Author: Daniel Walker, Colby Seeley, Adam Halliday
# Program to scrape general conference

from getpass import getpass
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import db
import sqlalchemy
import psycopg2


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


def scrape_conference():
    # Code to scrape general conference data and return a dataframe
    # Get the relevant church website for October 2025 General Conference
    response = requests.get(
        "https://www.churchofjesuschrist.org/study/general-conference/2025/10?lang=eng"
    )
    # Basically eliminate special character conversion problems with BeautifulSoup
    response.encoding = "utf-8"
    # Check to make sure scrape request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Grab all <li> tags that are specifically categorized as talks - very nice of the church to categorize for us
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
        # Loop through URLs, access relevant information and perform processing
        database_info = []
        for url in talk_urls:
            Conference_Response = requests.get(url)
            Conference_Response.encoding = 'utf-8'
            if Conference_Response.status_code == 200:
                conference_soup = BeautifulSoup(Conference_Response.text, "html.parser")
                ind_talk_items = conference_soup.find("h1")
                clean_title = ind_talk_items.get_text(strip=True)
                print(clean_title)
            else:
                print(f"Failed to retrieve the page. Status code: {Conference_Response.status_code}")
    else:
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
            # Variables with information needed for database connection
            db_user = "postgres"  # Your Postgres username (usually 'postgres')
            db_password = (
                "SchoolPaper2015"  # The password you use to log into pgAdmin/Postgres
            )
            db_host = "localhost"  # Usually 'localhost' if running on your own computer
            db_port = "5432"  # The default Postgres port
            db_name = "is303"  # The name of your database

            # 2. Build the connection string (the URL that points to your database)
            connection_string = (
                f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )

            # 3. Create the engine!
            engine = sqlalchemy.create_engine(connection_string)
            drop_table_query = sqlalchemy.text(
                "DROP table if exists general_conference;"
            )
            conn = engine.connect()
            conn.execute(drop_table_query)
            conn.commit()
            conn.close()
            # Perform the scraping process for general conference
            scrape_conference()
            # To save to the database, call oDatabase.insert_data(dataframe). Use this to save one row at a time please :)
        elif iUserChoice == "2":
            view_data()
        else:
            end_program()
