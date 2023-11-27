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

 # List of tournament csv's
tournamentsCsvList = ["A-Team-Europe_Africa-2019.csv",
"A-Team-Premier12-2019.csv",
"U-18-WorldCup-2017.csv",
"U-18-WorldCup-2019.csv",
"U-23-WorldCup-2018.csv"
]

# List to store the data of the tournaments
tournamentInfo = []

# Loop through csvlist and add all data to tournamentInfo 
for tournamentcsv in tournamentsCsvList:
    tournament = pd.read_csv(("tournaments/" + str(tournamentcsv)), sep=',')
    tournamentInfo.append(tournament)

# Combine all tournament info into dataframe and insert into database.
allTournamentsCombined = pd.concat(tournamentInfo)
allTournamentsCombined.to_sql(name="tournaments", con=SQL_Engine, if_exists='replace', index=False)
