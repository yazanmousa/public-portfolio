import pandas as pd
from sqlalchemy import create_engine

###################################
host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)
###################################

# Read csv files
mlb = pd.read_csv("mlbMilbScraper/allMlbPlayers.csv", sep=',')
milb = pd.read_csv("mlbMilbScraper/newAllMilbPlayers.csv", sep=',')

# Concat the dataframes
allPlayersCombined = pd.concat([mlb, milb], ignore_index=True)

# Insert combined dataframe to sql
allPlayersCombined.to_sql(name='allplayers', con=SQL_Engine, if_exists='replace', index=False)

import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']   (mergeCSV) All players have been inserted into database.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()