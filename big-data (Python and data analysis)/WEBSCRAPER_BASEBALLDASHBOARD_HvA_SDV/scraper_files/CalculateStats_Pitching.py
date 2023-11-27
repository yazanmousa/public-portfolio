
import pandas as pd
import numpy as np
from datetime import datetime
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

dfPitching_Gamelogs = pd.read_sql('db_Pitching_Gamelogs', SQL_Engine)
dfPitching_Summary = pd.read_sql('db_Pitching_Summary', SQL_Engine)
dfPitching_Yearly = pd.read_sql('db_Pitching_Yearly', SQL_Engine)
dfPitching_Career = pd.read_sql('db_Pitching_Career', SQL_Engine)

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

def Format_IP(df):
    if 'ip_label' not in df.columns:
        df.insert(df.columns.get_loc('ip_value')+1, 'ip_label', '0')

    for i in range(len(df)):
        Value = str(df['ip_value'][i])
        
        if '.' in Value:
            BaseValue = Value.split('.')[0]
            Decimal = int(Value.split('.')[1][:1])
        else:
            BaseValue = Value
            Decimal = int('0'[:1])
        
        if Decimal < 2 or Decimal >= 8:
            Label = str(BaseValue) + '.0'
        elif Decimal >= 2 and Decimal < 5:
            Label = str(BaseValue) + '.1'
        else:
            Label = str(BaseValue) + '.2'
        
        df['ip_label'][i] = Label
    return df

def Def_DateString(df):
    if 'MatchID' in df.columns:
        from datetime import datetime
        if 'DateString' not in df.columns:
            df.insert(df.columns.get_loc('Day')+1, 'DateString', '')

        for i in range(len(df)):
            DateObj = datetime.strptime((str(df['Year'][i]) + ' ' + str(df['Month'][i]) + ' ' + str(df['Day'][i])), "%Y %m %d")
            df['DateString'][i] = DateObj.strftime("%b %d, %Y")
    
    return df

def Calc_ERA(df):
    if 'era_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'era_value', float(0))
    
    if 'era_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'era_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if float(dfTemp['ip_value'][:i+1].sum()) == 0:
                            dfTemp['era_value'][i] = float(0)
                        else:
                            dfTemp['era_value'][i] = float(9 * dfTemp['er'][:i+1].sum() / float(dfTemp['ip_value'][:i+1].sum()))
                        
                        dfTemp['era_label'][i] = str(round(dfTemp['era_value'][i], 2))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if float(df['ip_value'][i]) == 0:
                df['era_value'][i] = float(0)
            else:
                df['era_value'][i] = float(9 * df['er'][i] / float(df['ip_value'][i]))
            
            df['era_label'][i] = str(round(df['era_value'][i], 2))

    return df

def Calc_WLP(df):
    if 'wlp_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'wlp_value', float(0))
    
    if 'wlp_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'wlp_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if (dfTemp['Win'][:i+1].sum() + dfTemp['Loss'][:i+1].sum()) == 0:
                            dfTemp['wlp_value'][i] = float(0)
                        else:
                            dfTemp['wlp_value'][i] = float(dfTemp['Win'][:i+1].sum() / (dfTemp['Win'][:i+1].sum() + dfTemp['Loss'][:i+1].sum()))
                        
                        dfTemp['wlp_label'][i] = Format_Label(dfTemp['wlp_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if (df['Win'][i] + df['Loss'][i]) == 0:
                df['wlp_value'][i] = float(0)
            else:
                df['wlp_value'][i] = float(df['Win'][i] / (df['Win'][i] + df['Loss'][i]))
            
            df['wlp_label'][i] = Format_Label(df['wlp_value'][i])

    return df

def Calc_WHIP(df):
    if 'whip_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'whip_value', float(0))
    
    if 'whip_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'whip_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ip_value'][:i+1].sum() == 0:
                            dfTemp['whip_value'][i] = float(0)
                        else:
                            dfTemp['whip_value'][i] = float((dfTemp['bb'][:i+1].sum() + dfTemp['h'][:i+1].sum()) / float(dfTemp['ip_value'][:i+1].sum()))
                        
                        dfTemp['whip_label'][i] = str(round(dfTemp['whip_value'][i], 3))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ip_value'][i] == 0:
                df['whip_value'][i] = float(0)
            else:
                df['whip_value'][i] = float((df['bb'][i] + df['h'][i]) / float(df['ip_value'][i]))
            
            df['whip_label'][i] = str(round(df['whip_value'][i], 3))

    return df

def Calc_H9(df):
    if 'h9_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'h9_value', float(0))
    
    if 'h9_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'h9_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ip_value'][:i+1].sum() == 0:
                            dfTemp['h9_value'][i] = float(0)
                        else:
                            dfTemp['h9_value'][i] = float(9 * dfTemp['h'][:i+1].sum() / float(dfTemp['ip_value'][:i+1].sum()))
                        
                        dfTemp['h9_label'][i] = str(round(dfTemp['h9_value'][i], 1))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ip_value'][i] == 0:
                df['h9_value'][i] = float(0)
            else:
                df['h9_value'][i] = float(9 * df['h'][i] / float(df['ip_value'][i]))
            
            df['h9_label'][i] = str(round(df['h9_value'][i], 1))

    return df

def Calc_BB9(df):
    if 'bb9_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'bb9_value', float(0))
    
    if 'bb9_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'bb9_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ip_value'][:i+1].sum() == 0:
                            dfTemp['bb9_value'][i] = float(0)
                        else:
                            dfTemp['bb9_value'][i] = float(9 * dfTemp['bb'][:i+1].sum() / float(dfTemp['ip_value'][:i+1].sum()))
                        
                        dfTemp['bb9_label'][i] = str(round(dfTemp['bb9_value'][i], 1))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ip_value'][i] == 0:
                df['bb9_value'][i] = float(0)
            else:
                df['bb9_value'][i] = float(9 * df['bb'][i] / float(df['ip_value'][i]))
            
            df['bb9_label'][i] = str(round(df['bb9_value'][i], 1))

    return df

def Calc_SO9(df):
    if 'so9_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'so9_value', float(0))
    
    if 'so9_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'so9_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ip_value'][:i+1].sum() == 0:
                            dfTemp['so9_value'][i] = float(0)
                        else:
                            dfTemp['so9_value'][i] = float(9 * dfTemp['so'][:i+1].sum() / float(dfTemp['ip_value'][:i+1].sum()))
                        
                        dfTemp['so9_label'][i] = str(round(dfTemp['so9_value'][i], 1))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ip_value'][i] == 0:
                df['so9_value'][i] = float(0)
            else:
                df['so9_value'][i] = float(9 * df['so'][i] / float(df['ip_value'][i]))
            
            df['so9_label'][i] = str(round(df['so9_value'][i], 1))

    return df

def Calc_SOBB(df):
    if 'sobb_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'sobb_value', float(0))
    
    if 'sobb_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'sobb_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['bb'][:i+1].sum() == 0:
                            dfTemp['sobb_value'][i] = float(0)
                        else:
                            dfTemp['sobb_value'][i] = float(dfTemp['so'][:i+1].sum() / dfTemp['bb'][:i+1].sum())
                        
                        dfTemp['sobb_label'][i] = str(round(dfTemp['sobb_value'][i], 1))
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['bb'][i] == 0:
                df['sobb_value'][i] = float(0)
            else:
                df['sobb_value'][i] = float(df['so'][i] / df['bb'][i])
            
            df['sobb_label'][i] = str(round(df['sobb_value'][i], 1))

    return df

def First_Latest_Appearance(df):
    if list(df.columns)[:2] == ['PlayerName', 'g'] or list(df.columns)[:2] == ['PlayerName', 'gs'] or list(df.columns)[:2] == ['PlayerName', 'FirstAppearance']:
        if 'FirstAppearance' not in df.columns:
            df.insert(1, 'FirstAppearance', '')

        if 'LatestAppearance' not in df.columns:
            df.insert(df.columns.get_loc('FirstAppearance')+1, 'LatestAppearance', '')

        for i in range(len(df['FirstAppearance'])):
            df1 = dfPitching_Gamelogs[dfPitching_Gamelogs['PlayerName'] == df['PlayerName'][i]].sort_values(['Year', 'Month', 'Day'], ascending=[True, True, True]).reset_index(drop=True)
            Year = str(int(df1['Year'][0]))
            MonthNo = datetime.strptime(str(int(df1['Month'][0])), "%m")
            MonthStr = MonthNo.strftime("%B")
            Day = str(int(df1['Day'][0]))
            
            if str(df1['HomeGame'][0]) == '1':
                HomeTeam = '<b>' + str(df1['Team'][0]) + '</b>'
                AwayTeam = str(df1['Opponent'][0])
            else:
                HomeTeam = str(df1['Opponent'][0])
                AwayTeam = '<b>' + str(df1['Team'][0]) + '</b>'
            df['FirstAppearance'][i] = MonthStr + ' ' + Day + ', ' + Year + ' (' + HomeTeam + ' - ' + AwayTeam + ')'
            
            df1 = dfPitching_Gamelogs[dfPitching_Gamelogs['PlayerName'] == df['PlayerName'][i]].sort_values(['Year', 'Month', 'Day'], ascending=[False, False, False]).reset_index(drop=True)
            Year = str(int(df1['Year'][0]))
            MonthNo = datetime.strptime(str(int(df1['Month'][0])), "%m")
            MonthStr = MonthNo.strftime("%B")
            Day = str(int(df1['Day'][0]))
            
            if str(df1['HomeGame'][0]) == '1':
                HomeTeam = '<b>' + str(df1['Team'][0]) + '</b>'
                AwayTeam = str(df1['Opponent'][0])
            else:
                HomeTeam = str(df1['Opponent'][0])
                AwayTeam = '<b>' + str(df1['Team'][0]) + '</b>'
            df['LatestAppearance'][i] = MonthStr + ' ' + Day + ', ' + Year + ' (' + HomeTeam + ' - ' + AwayTeam + ')'
    return df


dfPitching_Gamelogs = Def_DateString(dfPitching_Gamelogs)
dfPitching_Gamelogs = Format_IP(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_ERA(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_WLP(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_WHIP(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_H9(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_BB9(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_SO9(dfPitching_Gamelogs)
dfPitching_Gamelogs = Calc_SOBB(dfPitching_Gamelogs)
dfPitching_Gamelogs = First_Latest_Appearance(dfPitching_Gamelogs)

dfPitching_Summary = Format_IP(dfPitching_Summary)
dfPitching_Summary = Calc_ERA(dfPitching_Summary)
dfPitching_Summary = Calc_WLP(dfPitching_Summary)
dfPitching_Summary = Calc_WHIP(dfPitching_Summary)
dfPitching_Summary = Calc_H9(dfPitching_Summary)
dfPitching_Summary = Calc_BB9(dfPitching_Summary)
dfPitching_Summary = Calc_SO9(dfPitching_Summary)
dfPitching_Summary = Calc_SOBB(dfPitching_Summary)
dfPitching_Summary = First_Latest_Appearance(dfPitching_Summary)

dfPitching_Yearly = Format_IP(dfPitching_Yearly)
dfPitching_Yearly = Calc_ERA(dfPitching_Yearly)
dfPitching_Yearly = Calc_WLP(dfPitching_Yearly)
dfPitching_Yearly = Calc_WHIP(dfPitching_Yearly)
dfPitching_Yearly = Calc_H9(dfPitching_Yearly)
dfPitching_Yearly = Calc_BB9(dfPitching_Yearly)
dfPitching_Yearly = Calc_SO9(dfPitching_Yearly)
dfPitching_Yearly = Calc_SOBB(dfPitching_Yearly)
dfPitching_Yearly = First_Latest_Appearance(dfPitching_Yearly)

dfPitching_Career = Format_IP(dfPitching_Career)
dfPitching_Career = Calc_ERA(dfPitching_Career)
dfPitching_Career = Calc_WLP(dfPitching_Career)
dfPitching_Career = Calc_WHIP(dfPitching_Career)
dfPitching_Career = Calc_H9(dfPitching_Career)
dfPitching_Career = Calc_BB9(dfPitching_Career)
dfPitching_Career = Calc_SO9(dfPitching_Career)
dfPitching_Career = Calc_SOBB(dfPitching_Career)
dfPitching_Career = First_Latest_Appearance(dfPitching_Career)


dfPitching_Gamelogs.to_sql('db_Pitching_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Summary.to_sql('db_Pitching_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Yearly.to_sql('db_Pitching_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfPitching_Career.to_sql('db_Pitching_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)


filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Pitching statistics calculated.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

