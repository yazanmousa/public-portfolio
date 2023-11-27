
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

SQL_Engine = create_engine(os.getenv('SQL_Credentials'))


dfBatFld = pd.read_csv("Data_retrieval/Results/KNBSB_Batting.csv")

dfFielding = dfBatFld[["PlayerName", "Team", "Opponent", "League", "SeasonType", "HomeGame", "Year", "Month", "Day", "MatchID", "Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss"]]
dfBatting = dfBatFld

dfFielding = dfFielding.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)
dfBatting = dfBatting.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)

dfFielding.to_csv("Data_retrieval/Results/KNBSB_Fielding.csv", index=False)
dfBatting.to_csv("Data_retrieval/Results/KNBSB_Batting.csv", index=False)


Batting = ["Data_retrieval/Results/KNBSB_Batting.csv", "Data_retrieval/Results/Major_Batting.csv", "Data_retrieval/Results/Minor_Batting.csv"]
Fielding = ["Data_retrieval/Results/KNBSB_Fielding.csv", "Data_retrieval/Results/Major_Fielding.csv"]
Pitching = ["Data_retrieval/Results/KNBSB_Pitching.csv", "Data_retrieval/Results/Major_Pitching.csv", "Data_retrieval/Results/Minor_Pitching.csv"]

dfBatting = pd.DataFrame()
dfFielding = pd.DataFrame()
dfPitching = pd.DataFrame()

for df in Batting:
    dfBatting = dfBatting.replace([np.inf, -np.inf], np.nan)
    dfBatting = dfBatting.fillna(0)
    dfBatting = pd.concat([dfBatting, pd.read_csv(df)]).reset_index(drop=True)

for df in Fielding:
    dfFielding = dfFielding.replace([np.inf, -np.inf], np.nan)
    dfFielding = dfFielding.fillna(0)
    dfFielding = pd.concat([dfFielding, pd.read_csv(df)]).reset_index(drop=True)

for df in Pitching:
    dfPitching = dfPitching.replace([np.inf, -np.inf], np.nan)
    dfPitching = dfPitching.fillna(0)
    dfPitching = pd.concat([dfPitching, pd.read_csv(df)]).reset_index(drop=True)


ColsAsStrings = ["PlayerName", "Team", "Opponent", "League", "SeasonType", "ip"]

for Column in ColsAsStrings:
    for df in [dfBatting, dfFielding, dfPitching]:
        if Column in df.columns:
            df[Column] = df[Column].astype(str)


Batting_ColsAsIntegers = ["HomeGame", "Year", "Month", "Day", "MatchID", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "gdp", "Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss"]
Fielding_ColsAsIntegers = ["HomeGame", "Year", "Month", "Day", "MatchID", "po", "a", "e", "Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss"]
Pitching_ColsAsIntegers = ["HomeGame", "Year", "Month", "Day", "MatchID", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save"]

for Column in Batting_ColsAsIntegers:
    dfBatting[Column] = dfBatting[Column].replace([np.inf, -np.inf], np.nan)
    dfBatting[Column] = dfBatting[Column].fillna(0)
    dfBatting[Column] = dfBatting[Column].astype(int)

for Column in Fielding_ColsAsIntegers:
    dfFielding[Column] = dfFielding[Column].replace([np.inf, -np.inf], np.nan)
    dfFielding[Column] = dfFielding[Column].fillna(0)
    dfFielding[Column] = dfFielding[Column].astype(int)

for Column in Pitching_ColsAsIntegers:
    dfPitching[Column] = dfPitching[Column].replace([np.inf, -np.inf], np.nan)
    dfPitching[Column] = dfPitching[Column].fillna(0)
    dfPitching[Column] = dfPitching[Column].astype(int)

dfBatting = dfBatting.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True))
dfFielding = dfFielding.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True))
dfPitching = dfPitching.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True))


dfBatting.to_sql('db_Batting_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding.to_sql('db_Fielding_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching.to_sql('db_Pitching_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)


import os, shutil
CurrentPath = os.path.dirname(os.path.realpath(__file__))
ResultsPath = CurrentPath[:CurrentPath.rfind('/')] + '/Results'
for filename in os.listdir(ResultsPath):
    file_path = os.path.join(ResultsPath, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        pass


import datetime
filename = './Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    All temporary CSV files combined and sent to MySQL database.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()