from sqlalchemy import create_engine
import pandas as pd
from pandas import read_sql

# Define MySQL info
host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)

import os

os.environ['SQL_Credentials'] = config

def load_SQL_table(SQL_Statement):
    df = read_sql(SQL_Statement, SQL_Engine)
    return df

def execute_command(SQL_Statement):
    SQL_Engine.connect().execute(SQL_Statement)

# df_batting = pd.read_sql_table('Player', SQL_Engine)
# df_batting.rename(columns={'fullName': 'playername', 'id' : 'ID'}, inplace=True)
# df_batting=df_batting[{'playername', 'ID'}]
# df_batting.columns = map(lambda x: str(x).upper(), df_batting.columns)
# df_batting['PLAYERNAME'] = df_batting['PLAYERNAME'].astype('category')

# len(df_batting)


# df_batting2 = pd.read_sql_table('allplayers', SQL_Engine)
# df_batting2.rename(columns={'Name': 'playername', 'Id' : 'ID'}, inplace=True)
# df_batting2=df_batting2[{'playername', 'ID'}]
# df_batting2.columns = map(lambda x: str(x).upper(), df_batting2.columns)
# df_batting2['PLAYERNAME'] = df_batting2['PLAYERNAME'].astype('category')


# len(df_batting2)

# total_batting = pd.concat([df_batting, df_batting2], ignore_index=True)
# len(total_batting)

# total_batting.drop_duplicates(keep="first", inplace=True, subset=['ID'])
# len(total_batting)