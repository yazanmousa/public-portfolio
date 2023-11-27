
import pandas as pd
import numpy as np
import operator
from sqlalchemy import create_engine
import os


###################################
# Define MySQL info
host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)
###################################

dfFielding_Gamelogs = pd.read_sql('db_Fielding_Gamelogs', SQL_Engine)
dfFielding_Summary = pd.read_sql('db_Fielding_Summary', SQL_Engine)
dfFielding_Yearly = pd.read_sql('db_Fielding_Yearly', SQL_Engine)
dfFielding_Career = pd.read_sql('db_Fielding_Career', SQL_Engine)

def Format_Label(value):
    value = str(value)
    if '.' in value:
        BaseValue = value.split('.')[0]
        Decimal = value.split('.')[1]
    else:
        BaseValue = '0'
        Decimal = '0'

    if BaseValue == '1':
        label = '1.000'
    else:
        if len(Decimal) < 3:
            for x in range(3 - len(Decimal)):
                x = x # useless but prevents an 'unused variable' error
                Decimal = Decimal + '0'
        else:
            Decimal = Decimal[:3]

        label = '.' + Decimal

    return label

def Def_DateString(df):
    if 'MatchID' in df.columns:
        from datetime import datetime
        if 'DateString' not in df.columns:
            df.insert(df.columns.get_loc('Day')+1, 'DateString', '')

        for i in range(len(df)):
            DateObj = datetime.strptime((str(df['Year'][i]) + ' ' + str(df['Month'][i]) + ' ' + str(df['Day'][i])), "%Y %m %d")
            df['DateString'][i] = DateObj.strftime("%b %d, %Y")
    
    return df

def Calc_DefChances(df):
    if 'ch' not in df.columns:
        df.insert(df.columns.get_loc('e')+1, 'ch', 0)

    for i in range(len(df)):
        df['ch'][i] = df['po'][i] + df['a'][i] + df['e'][i]
    
    return df

def Calc_FieldingAverage(df):
    if 'favg_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'favg_value', float(0))
    
    if 'favg_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'favg_label', '0')

    if 'MatchID' in list(df.columns):
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ch'][:i+1].sum() == 0:
                            dfTemp['favg_value'][i] = float(0)
                        else:
                            dfTemp['favg_value'][i] = float((dfTemp['po'][:i+1].sum() + dfTemp['a'][:i+1].sum()) / dfTemp['ch'][:i+1].sum())
                        
                        dfTemp['favg_label'][i] = Format_Label(dfTemp['favg_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        return df2
    else:
        for i in range(len(df)):
            if df['ch'][i] == 0:
                df['favg_value'][i] = float(0)
            else:
                df['favg_value'][i] = float((df['po'][i] + df['a'][i]) / df['ch'][i])
            
            df['favg_label'][i] = Format_Label(df['favg_value'][i])

        return df

def Calc_MainPosition(df):
    if 'MatchID' not in df.columns:
        if 'MainPos' not in df.columns:
            df.insert(df.columns.get_loc('Pos_1b'), 'MainPos', '')
        
        for i in range(len(df['MainPos'])):
            Pos_1b = df['Pos_1b'][i]
            Pos_2b = df['Pos_2b'][i]
            Pos_3b = df['Pos_3b'][i]
            Pos_ss = df['Pos_ss'][i]
            Pos_lf = df['Pos_lf'][i]
            Pos_cf = df['Pos_cf'][i]
            Pos_rf = df['Pos_rf'][i]
            Pos_c = df['Pos_c'][i]
            Pos_p = df['Pos_p'][i]
            Pos_dh = df['Pos_dh'][i]
            Pos_ph = df['Pos_ph'][i]
            Pos_pr = df['Pos_pr'][i]

            PosNames = ['First Baseman', 'Second Baseman', 'Third Baseman', 'Shortstop', 'Left Fielder', 'Center Fielder', 'Right Fielder', 'Catcher', 'Pitcher', 'Designated Hitter', 'Pinch Hitter', 'Pinch Runner']
            PosCount = [Pos_1b, Pos_2b, Pos_3b, Pos_ss, Pos_lf, Pos_cf, Pos_rf, Pos_c, Pos_p, Pos_dh, Pos_ph, Pos_pr]
            PosDict = dict(zip(PosNames, PosCount))
            df['MainPos'][i] = max(PosDict.items(), key=operator.itemgetter(1))[0]
    
    if 'MatchID' in df.columns:
        if 'PosString' not in df.columns:
            df.insert(df.columns.get_loc('Pos_1b'), 'PosString', '')
        
        for i in range(len(df['PosString'])):
            Pos_1b = df['Pos_1b'][i]
            Pos_2b = df['Pos_2b'][i]
            Pos_3b = df['Pos_3b'][i]
            Pos_ss = df['Pos_ss'][i]
            Pos_lf = df['Pos_lf'][i]
            Pos_cf = df['Pos_cf'][i]
            Pos_rf = df['Pos_rf'][i]
            Pos_c = df['Pos_c'][i]
            Pos_p = df['Pos_p'][i]
            Pos_dh = df['Pos_dh'][i]
            Pos_ph = df['Pos_ph'][i]
            Pos_pr = df['Pos_pr'][i]

            PosNames = ['1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'C', 'P', 'DH', 'PH', 'PR']
            PosCount = [Pos_1b, Pos_2b, Pos_3b, Pos_ss, Pos_lf, Pos_cf, Pos_rf, Pos_c, Pos_p, Pos_dh, Pos_ph, Pos_pr]
            PosDict = dict(zip(PosNames, PosCount))
            df['PosString'][i] = max(PosDict.items(), key=operator.itemgetter(1))[0]

    return df
 

dfFielding_Gamelogs = Def_DateString(dfFielding_Gamelogs)
dfFielding_Gamelogs = Calc_DefChances(dfFielding_Gamelogs)
dfFielding_Gamelogs = Calc_FieldingAverage(dfFielding_Gamelogs)
dfFielding_Gamelogs = Calc_MainPosition(dfFielding_Gamelogs)
    
dfFielding_Summary = Calc_DefChances(dfFielding_Summary)
dfFielding_Summary = Calc_FieldingAverage(dfFielding_Summary)
dfFielding_Summary = Calc_MainPosition(dfFielding_Summary)
    
dfFielding_Yearly = Calc_DefChances(dfFielding_Yearly)
dfFielding_Yearly = Calc_FieldingAverage(dfFielding_Yearly)
dfFielding_Yearly = Calc_MainPosition(dfFielding_Yearly)
    
dfFielding_Career = Calc_DefChances(dfFielding_Career)
dfFielding_Career = Calc_FieldingAverage(dfFielding_Career)
dfFielding_Career = Calc_MainPosition(dfFielding_Career)


dfFielding_Gamelogs.to_sql('db_Fielding_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Summary.to_sql('db_Fielding_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Yearly.to_sql('db_Fielding_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfFielding_Career.to_sql('db_Fielding_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)


import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Fielding statistics calculated.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

