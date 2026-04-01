#Author: Daniel Walker
#Manages all database functions for the conference scraping project

import sqlalchemy
import pandas as pd


class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = sqlalchemy.create_engine(connection_string)

    def insert_data(self, dataframe: pd.DataFrame):
        dataframe.to_sql('general_conference', con=self.engine, if_exists='append', index=False)

    def get_all_talks(self):
        # Code to retrieve all talks from the database
        pass

    def get_talk_by_id(self, talk_id):
        # Code to retrieve a specific talk by its ID
        pass

    def drop_tables(self):
        self.engine.connect().execute(sqlalchemy.text("DROP TABLE IF EXISTS general_conference"))
