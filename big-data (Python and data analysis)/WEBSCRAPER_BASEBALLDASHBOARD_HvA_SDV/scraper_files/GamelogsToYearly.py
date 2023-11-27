
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

SQL_Engine = create_engine(os.getenv('SQL_Credentials'))

dfBatting = pd.read_sql('db_Batting_Gamelogs', SQL_Engine)
dfFielding = pd.read_sql('db_Fielding_Gamelogs', SQL_Engine)
dfPitching = pd.read_sql('db_Pitching_Gamelogs', SQL_Engine)


# Caculate Games Played
GamesPlayed_Batting_Yearly = dfBatting.groupby(['PlayerName', 'League', 'Year'], as_index=False).count()[['PlayerName', 'League', 'Year', 'Opponent']]
GamesPlayed_Batting_Yearly.columns = ['PlayerName', 'League', 'Year', 'g']

GamesPlayed_Batting_Summary = dfBatting.groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).count()[['PlayerName', 'Team', 'League', 'Year', 'Opponent']]
GamesPlayed_Batting_Summary.columns = ['PlayerName', 'Team', 'League', 'Year', 'g']

GamesPlayed_Batting_Career = dfBatting.groupby(['PlayerName'], as_index=False).count()[['PlayerName', 'Opponent']]
GamesPlayed_Batting_Career.columns = ['PlayerName', 'g']


GamesPlayed_Fielding_Yearly = dfFielding.groupby(['PlayerName', 'League', 'Year'], as_index=False).count()[['PlayerName', 'League', 'Year', 'Opponent']]
GamesPlayed_Fielding_Yearly.columns = ['PlayerName', 'League', 'Year', 'g']

GamesPlayed_Fielding_Summary = dfFielding.groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).count()[['PlayerName', 'Team', 'League', 'Year', 'Opponent']]
GamesPlayed_Fielding_Summary.columns = ['PlayerName', 'Team', 'League', 'Year', 'g']

GamesPlayed_Fielding_Career = dfFielding.groupby(['PlayerName'], as_index=False).count()[['PlayerName', 'Opponent']]
GamesPlayed_Fielding_Career.columns = ['PlayerName', 'g']


GamesPlayed_Pitching_Yearly = dfPitching.groupby(['PlayerName', 'League', 'Year'], as_index=False).count()[['PlayerName', 'League', 'Year', 'Opponent']]
GamesPlayed_Pitching_Yearly.columns = ['PlayerName', 'League', 'Year', 'g']

GamesPlayed_Pitching_Summary = dfPitching.groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).count()[['PlayerName', 'Team', 'League', 'Year', 'Opponent']]
GamesPlayed_Pitching_Summary.columns = ['PlayerName', 'Team', 'League', 'Year', 'g']

GamesPlayed_Pitching_Career = dfPitching.groupby(['PlayerName'], as_index=False).count()[['PlayerName', 'Opponent']]
GamesPlayed_Pitching_Career.columns = ['PlayerName', 'g']


dfPitching = dfPitching.rename(columns={"ip": "ip_label"})
dfPitching["ip_label"] = dfPitching["ip_label"].astype(str)
dfPitching.insert(11, "ip_value", 0)

dfPitching["ip_value"] = dfPitching["ip_value"].astype(float)

for i in range(len(dfPitching)):
    Value = str(dfPitching['ip_label'][i])
    if '.' in Value:
        BaseValue = Value.split('.')[0]
        Decimal = Value.split('.')[1]
    else:
        BaseValue = Value
        Decimal = '0'

    if Decimal == '1':
        NewValue = float(BaseValue) + (1/3)
    elif Decimal == '2':
        NewValue = float(BaseValue) + (2/3)
    else:
        NewValue = float(BaseValue)
    
    dfPitching['ip_value'][i] = float(NewValue)

dfPitching["ip_value"] = dfPitching["ip_value"].astype(float)


dfBatting_Yearly = dfBatting.groupby(['PlayerName', 'Year', 'League'], as_index=False).sum()
dfBatting_Yearly = dfBatting_Yearly.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfBatting_Yearly.columns)
ColList.insert(dfBatting_Yearly.columns.get_loc('ab'), 'g')
dfBatting_Yearly = dfBatting_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
GamesPlayed_Batting_Yearly = GamesPlayed_Batting_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
dfBatting_Yearly = pd.concat([dfBatting_Yearly, GamesPlayed_Batting_Yearly[['g']]], axis=1)
dfBatting_Yearly = dfBatting_Yearly[ColList]
dfBatting_Yearly = dfBatting_Yearly.sort_values(['PlayerName', 'Year', 'League'], ascending=[True, True, True]).reset_index(drop=True)

dfFielding_Yearly = dfFielding.groupby(['PlayerName', 'Year', 'League'], as_index=False).sum()
dfFielding_Yearly = dfFielding_Yearly.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfFielding_Yearly.columns)
ColList.insert(dfFielding_Yearly.columns.get_loc('po'), 'g')
dfFielding_Yearly = dfFielding_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
GamesPlayed_Fielding_Yearly = GamesPlayed_Fielding_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
dfFielding_Yearly = pd.concat([dfFielding_Yearly, GamesPlayed_Fielding_Yearly[['g']]], axis=1)
dfFielding_Yearly = dfFielding_Yearly[ColList]
dfFielding_Yearly = dfFielding_Yearly.sort_values(['PlayerName', 'Year', 'League'], ascending=[True, True, True]).reset_index(drop=True)

dfPitching_Yearly = dfPitching.groupby(['PlayerName', 'Year', 'League'], as_index=False).sum()
dfPitching_Yearly = dfPitching_Yearly.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfPitching_Yearly.columns)
ColList.insert(dfPitching_Yearly.columns.get_loc('ip_value'), 'g')
dfPitching_Yearly = dfPitching_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
GamesPlayed_Pitching_Yearly = GamesPlayed_Pitching_Yearly.sort_values(['PlayerName', 'League', 'Year'], ascending=[True, True, True]).reset_index(drop=True)
dfPitching_Yearly = pd.concat([dfPitching_Yearly, GamesPlayed_Pitching_Yearly[['g']]], axis=1)
dfPitching_Yearly = dfPitching_Yearly[ColList]
dfPitching_Yearly = dfPitching_Yearly.sort_values(['PlayerName', 'Year', 'League'], ascending=[True, True, True]).reset_index(drop=True)

dfBatting_Yearly.to_sql('db_Batting_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Yearly.to_sql('db_Fielding_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Yearly.to_sql('db_Pitching_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)



dfBatting_Summary = dfBatting.sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True).groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).sum()
dfBatting_Summary = dfBatting_Summary.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfBatting_Summary.columns)
ColList.insert(dfBatting_Summary.columns.get_loc('ab'), 'g')
dfBatting_Summary = dfBatting_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
GamesPlayed_Batting_Summary = GamesPlayed_Batting_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
dfBatting_Summary = pd.concat([dfBatting_Summary, GamesPlayed_Batting_Summary[['g']]], axis=1)
dfBatting_Summary = dfBatting_Summary[ColList]
dfBatting_Summary = dfBatting_Summary.sort_values(['PlayerName', 'Year', 'Team'], ascending=[True, True, True]).reset_index(drop=True)

dfFielding_Summary = dfFielding.sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True).groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).sum()
dfFielding_Summary = dfFielding_Summary.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfFielding_Summary.columns)
ColList.insert(dfFielding_Summary.columns.get_loc('po'), 'g')
dfFielding_Summary = dfFielding_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
GamesPlayed_Fielding_Summary = GamesPlayed_Fielding_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
dfFielding_Summary = pd.concat([dfFielding_Summary, GamesPlayed_Fielding_Summary[['g']]], axis=1)
dfFielding_Summary = dfFielding_Summary[ColList]
dfFielding_Summary = dfFielding_Summary.sort_values(['PlayerName', 'Year', 'Team'], ascending=[True, True, True]).reset_index(drop=True)

dfPitching_Summary = dfPitching.sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True).groupby(['PlayerName', 'Team', 'League', 'Year'], as_index=False).sum()
dfPitching_Summary = dfPitching_Summary.drop(['HomeGame', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfPitching_Summary.columns)
ColList.insert(dfPitching_Summary.columns.get_loc('ip_value'), 'g')
dfPitching_Summary = dfPitching_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
GamesPlayed_Pitching_Summary = GamesPlayed_Pitching_Summary.sort_values(['PlayerName', 'Team', 'League', 'Year'], ascending=[True, True, True, True]).reset_index(drop=True)
dfPitching_Summary = pd.concat([dfPitching_Summary, GamesPlayed_Pitching_Summary[['g']]], axis=1)
dfPitching_Summary = dfPitching_Summary[ColList]
dfPitching_Summary = dfPitching_Summary.sort_values(['PlayerName', 'Year', 'Team'], ascending=[True, True, True]).reset_index(drop=True)

dfBatting_Summary.to_sql('db_Batting_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Summary.to_sql('db_Fielding_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Summary.to_sql('db_Pitching_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)



dfBatting_Career = dfBatting.groupby(['PlayerName'], as_index=False).sum()
dfBatting_Career = dfBatting_Career.drop(['HomeGame', 'Year', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfBatting_Career.columns)
ColList.insert(dfBatting_Career.columns.get_loc('ab'), 'g')
dfBatting_Career = dfBatting_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
GamesPlayed_Batting_Career = GamesPlayed_Batting_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
dfBatting_Career = pd.concat([dfBatting_Career, GamesPlayed_Batting_Career[['g']]], axis=1)
dfBatting_Career = dfBatting_Career[ColList]
dfBatting_Career = dfBatting_Career.sort_values(['PlayerName'], ascending=[True]).reset_index(drop=True)

dfFielding_Career = dfFielding.groupby(['PlayerName'], as_index=False).sum()
dfFielding_Career = dfFielding_Career.drop(['HomeGame', 'Year', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfFielding_Career.columns)
ColList.insert(dfFielding_Career.columns.get_loc('po'), 'g')
dfFielding_Career = dfFielding_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
GamesPlayed_Fielding_Career = GamesPlayed_Fielding_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
dfFielding_Career = pd.concat([dfFielding_Career, GamesPlayed_Fielding_Career[['g']]], axis=1)
dfFielding_Career = dfFielding_Career[ColList]
dfFielding_Career = dfFielding_Career.sort_values(['PlayerName'], ascending=[True]).reset_index(drop=True)

dfPitching_Career = dfPitching.groupby(['PlayerName'], as_index=False).sum()
dfPitching_Career = dfPitching_Career.drop(['HomeGame', 'Year', 'Month', 'Day', 'MatchID'], axis=1)
ColList = list(dfPitching_Career.columns)
ColList.insert(dfPitching_Career.columns.get_loc('ip_value'), 'g')
dfPitching_Career = dfPitching_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
GamesPlayed_Pitching_Career = GamesPlayed_Pitching_Career.sort_values(['PlayerName'], ascending=True).reset_index(drop=True)
dfPitching_Career = pd.concat([dfPitching_Career, GamesPlayed_Pitching_Career[['g']]], axis=1)
dfPitching_Career = dfPitching_Career[ColList]
dfPitching_Career = dfPitching_Career.sort_values(['PlayerName'], ascending=[True]).reset_index(drop=True)

dfBatting_Career.to_sql('db_Batting_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Career.to_sql('db_Fielding_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Career.to_sql('db_Pitching_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)


dfBatting.to_sql('db_Batting_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding.to_sql('db_Fielding_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching.to_sql('db_Pitching_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)



import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Gamelog tables converted to yearly, summary and career tables.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

