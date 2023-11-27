from sqlalchemy import create_engine
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
