# Author: Daniel Walker, Colby Seeley, Adam Halliday
# Program to scrape general conference

from getpass import getpass
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import db

#This function is specifically because of permissions issues for the database (for Daniel lol).
def database_init():
    db_user = input("Enter Postgres Username (usually 'postgres'): ")
    db_password = getpass("Enter Postgres Password: ")
    db_host = "localhost"
    db_port = "5432"
    db_name = "is303"
    oDatabase = db.DatabaseManager(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    return oDatabase

def scrape_conference():
    # Code to scrape general conference data and return a dataframe
    pass

#View summaries of the data
def view_data():
    while True:
        iUserChoice = input("\nYou selected to see summaries. Enter 1 to see a summary of all talks. Enter 2 to select a specific talk. Enter anything else to exit: ")
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
        print("\n"*2)
        print("="*50)
        print("Welcome to the General Conference Scraper!")
        iUserChoice = input("If you want to scrape data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program:")
        if iUserChoice == "1":
            scrape_conference()
            #To save to the database, call oDatabase.insert_data(dataframe). Use this to save one row at a time please :)
        elif iUserChoice == "2":
            view_data()
        else:
            end_program()
            