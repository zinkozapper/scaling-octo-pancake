#Author: Daniel Walker, Colby Seeley
#Manages all database functions for the conference scraping project

import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plot


class DatabaseManager:
    def __init__( self, db_password, db_user: str = "postgres", db_host: str = "localhost", db_port: int = 5432, db_name: str = "IS303" ):        
        self.connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = sqlalchemy.create_engine(self.connection_string)

    def insert_data(self, dataframe: pd.DataFrame):
        dataframe.to_sql('general_conference', con=self.engine, if_exists='append', index=False)

    def get_all_talks(self):
        # Code to retrieve all talks from the database
        sql_query = 'SELECT * FROM general_conference'
        df_from_postgres = pd.read_sql_query(sql_query, self.engine)

        # Convert to numeric to handle database-stored NaN/NULL values. sum() breaks with non-numbers like 'N/A' but knows to ignore NaN
        df_numeric = df_from_postgres.drop(['Speaker_Name', 'Talk_Name', 'Kicker'], axis=1).apply(pd.to_numeric, errors='coerce')
        df_sums = df_numeric.sum()
        df_sums_filtered = df_sums[df_sums > 2]

        df_sums_filtered.plot(kind='bar')
        plot.title('Standard Works Referenced in General Conference')
        plot.xlabel('Standard Works Books')
        plot.ylabel('# Times Referenced')
        plot.show()

        print("The graphical summary of all talks has been successfully created.")
        
    def get_talk_by_id(self):
        # Code to retrieve a specific talk by its ID

        #Still need full df so we can search it later
        sql_query = 'SELECT * FROM general_conference'
        df_from_postgres = pd.read_sql_query(sql_query, self.engine)
        #create searchable dictionary from df
        dict_talk_list = df_from_postgres.to_dict('index')

        print("\nThe following are the names of speakers and their talks: ")
        print(". "*42)
        df_display = pd.read_sql('SELECT "Speaker_Name", "Talk_Name" FROM general_conference', self.engine)
        df_display.index += 1  # Shifts the pandas index to start at 1
        print(df_display)
        print(". "*42)
        print("Please enter the number (#) of the talk you want to see summarized: ")

        #handle user input to be an integer on the talk list
        len(dict_talk_list)
        while True:
            try:
                i_talk_choice = int(input())
                if i_talk_choice >= 1 and i_talk_choice <= len(dict_talk_list):
                    break
                else:
                    print(f"Input must be between 1 and {len(dict_talk_list)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyError:
                print("Invalid talk number. Please enter a valid number.")
        for talk in dict_talk_list:
            if (i_talk_choice - 1) == talk:
                s_talk_name = dict_talk_list[talk]['Talk_Name']
                df_choice = df_from_postgres.query(f"Talk_Name == '{s_talk_name}'")
                df_numeric = df_choice.drop(['Speaker_Name', 'Talk_Name', 'Kicker'], axis=1).apply(pd.to_numeric, errors='coerce')
                df_sums = df_numeric.sum()
                df_sums_filtered = df_sums[df_sums > 0]
                # CHECK IF DATAFRAME IS EMPTY
                if df_sums_filtered.empty:
                    print(f"\n--> The talk '{s_talk_name}' has no scriptural references. No graph could be generated.")
                    return
                df_sums_filtered.plot(kind='bar')
                plot.title(f'Standard Works Referenced in {s_talk_name}')
                plot.xlabel('Standard Works Books')
                plot.ylabel('# Times Referenced')
                plot.show()
                return

    def drop_tables(self):
        with self.engine.connect() as connection: 
            connection.execute(sqlalchemy.text("DROP TABLE IF EXISTS general_conference"))
    
            connection.commit()
