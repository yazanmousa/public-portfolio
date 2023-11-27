
import pandas as pd
import numpy as np
import operator
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

dfBatting_Gamelogs = pd.read_sql('db_Batting_Gamelogs', SQL_Engine)
dfBatting_Summary = pd.read_sql('db_Batting_Summary', SQL_Engine)
dfBatting_Yearly = pd.read_sql('db_Batting_Yearly', SQL_Engine)
dfBatting_Career = pd.read_sql('db_Batting_Career', SQL_Engine)


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

def Calc_PA(df):
    if 'pa' not in df.columns:
        df.insert(df.columns.get_loc('ab'), 'pa', 0)

    for i in range(len(df)):
        df['pa'][i] = df['ab'][i] + df['bb'][i] + df['hbp'][i] + df['sh'][i] + df['sf'][i] + df['ibb'][i]
    
    return df

def Calc_AVG(df):
    if 'avg_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'avg_value', float(0))
    
    if 'avg_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'avg_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ab'][:i+1].sum() == 0:
                            dfTemp['avg_value'][i] = float(0)
                        else:
                            dfTemp['avg_value'][i] = float(dfTemp['h'][:i+1].sum() / dfTemp['ab'][:i+1].sum())
                        
                        dfTemp['avg_label'][i] = Format_Label(dfTemp['avg_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    if 'MatchID' not in df.columns:
        for i in range(len(df)):
            if df['ab'][i] == 0:
                df['avg_value'][i] = float(0)
            else:
                df['avg_value'][i] = float(df['h'][i] / df['ab'][i])
            
            df['avg_label'][i] = Format_Label(df['avg_value'][i])

    return df

def Calc_OBP(df):
    if 'obp_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'obp_value', float(0))
    
    if 'obp_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'obp_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if (dfTemp['ab'][:i+1].sum() + dfTemp['bb'][:i+1].sum() + dfTemp['ibb'][:i+1].sum() + dfTemp['hbp'][:i+1].sum() + dfTemp['sf'][:i+1].sum() + dfTemp['sh'][:i+1].sum()) == 0:
                            dfTemp['obp_value'][i] = float(0)
                        else:
                            dfTemp['obp_value'][i] = float((dfTemp['h'][:i+1].sum() + dfTemp['bb'][:i+1].sum() + dfTemp['ibb'][:i+1].sum() + dfTemp['hbp'][:i+1].sum()) / (dfTemp['ab'][:i+1].sum() + dfTemp['bb'][:i+1].sum() + dfTemp['ibb'][:i+1].sum() + dfTemp['hbp'][:i+1].sum() + dfTemp['sf'][:i+1].sum() + dfTemp['sh'][:i+1].sum()))
                        
                        dfTemp['obp_label'][i] = Format_Label(dfTemp['obp_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if (df['ab'][:i+1].sum() + df['bb'][:i+1].sum() + df['ibb'][:i+1].sum() + df['hbp'][:i+1].sum() + df['sf'][:i+1].sum() + df['sh'][:i+1].sum()) == 0:
                df['obp_value'][i] = float(0)
            else:
                df['obp_value'][i] = float((df['h'][:i+1].sum() + df['bb'][:i+1].sum() + df['ibb'][:i+1].sum() + df['hbp'][:i+1].sum()) / (df['ab'][:i+1].sum() + df['bb'][:i+1].sum() + df['ibb'][:i+1].sum() + df['hbp'][:i+1].sum() + df['sf'][:i+1].sum() + df['sh'][:i+1].sum()))
            
            df['obp_label'][i] = Format_Label(df['obp_value'][i])

    return df

def Calc_SLG(df):
    if 'slg_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'slg_value', float(0))
    
    if 'slg_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'slg_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ab'][:i+1].sum() == 0:
                            dfTemp['slg_value'][i] = float(0)
                        else:
                            dfTemp['slg_value'][i] = float(((dfTemp['h'][:i+1].sum() - dfTemp['2b'][:i+1].sum() - dfTemp['3b'][:i+1].sum() - dfTemp['hr'][:i+1].sum()) + (2 * dfTemp['2b'][:i+1].sum()) + (3 * dfTemp['3b'][:i+1].sum()) + (4 * dfTemp['hr'][:i+1].sum())) / dfTemp['ab'][:i+1].sum())
                        
                        dfTemp['slg_label'][i] = Format_Label(dfTemp['slg_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ab'][i] == 0:
                df['slg_value'][i] = float(0)
            else:
                df['slg_value'][i] = float(((df['h'][i] - df['2b'][i] - df['3b'][i] - df['hr'][i]) + (2 * df['2b'][i]) + (3 * df['3b'][i]) + (4 * df['hr'][i])) / df['ab'][i])
            
            df['slg_label'][i] = Format_Label(df['slg_value'][i])

    return df

def Calc_OPS(df):
    if 'ops_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'ops_value', float(0))
    
    if 'ops_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'ops_label', '0')

    if 'MatchID' in df.columns:
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if (dfTemp['obp_value'][:i+1].sum() + dfTemp['slg_value'][:i+1].sum()) == 0:
                            dfTemp['ops_value'][i] = float(0)
                        else:
                            dfTemp['ops_value'][i] = float(((dfTemp['h'][:i+1].sum() + dfTemp['bb'][:i+1].sum() + dfTemp['ibb'][:i+1].sum() + dfTemp['hbp'][:i+1].sum()) / (dfTemp['ab'][:i+1].sum() + dfTemp['bb'][:i+1].sum() + dfTemp['ibb'][:i+1].sum() + dfTemp['hbp'][:i+1].sum() + dfTemp['sf'][:i+1].sum() + dfTemp['sh'][:i+1].sum())) + (((dfTemp['h'][:i+1].sum() - dfTemp['2b'][:i+1].sum() - dfTemp['3b'][:i+1].sum() - dfTemp['hr'][:i+1].sum()) + (2 * dfTemp['2b'][:i+1].sum()) + (3 * dfTemp['3b'][:i+1].sum()) + (4 * dfTemp['hr'][:i+1].sum())) / dfTemp['ab'][:i+1].sum()))
                        
                        dfTemp['ops_label'][i] = Format_Label(dfTemp['ops_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['obp_value'][i] == 0 and df['slg_value'][i] == 0:
                df['ops_value'][i] = float(0)
            else:
                df['ops_value'][i] = float(((df['h'][i] + df['bb'][i] + df['ibb'][i] + df['hbp'][i]) / (df['ab'][i] + df['bb'][i] + df['ibb'][i] + df['hbp'][i] + df['sf'][i] + df['sh'][i])) + (((df['h'][i] - df['2b'][i] - df['3b'][i] - df['hr'][i]) + (2 * df['2b'][i]) + (3 * df['3b'][i]) + (4 * df['hr'][i])) / df['ab'][i]))
            
            df['ops_label'][i] = Format_Label(df['ops_value'][i])

    return df

def Calc_ISO(df):
    if 'iso_value' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'iso_value', float(0))
    
    if 'iso_label' not in df.columns:
        NoOfCols = len(df.columns)
        df.insert(NoOfCols, 'iso_label', '0')

    if 'MatchID' in df.columns:
        print('Start gamelogs')
        df2 = pd.DataFrame()
        for PlayerName in df['PlayerName'].unique().tolist():
            dfTemp_start = df[df['PlayerName'] == PlayerName].sort_values(['PlayerName', 'Year', 'Month', 'Day'], ascending=[True, True, True, True]).reset_index(drop=True)
            for Year in dfTemp_start['Year'].unique().tolist():
                dfTemp_year = dfTemp_start[dfTemp_start['Year'] == Year].reset_index(drop=True)
                for Team in dfTemp_year['Team'].unique().tolist():
                    dfTemp = dfTemp_year[dfTemp_year['Team'] == Team].reset_index(drop=True)
                    for i in range(len(dfTemp)):
                        if dfTemp['ab'][:i+1].sum() == 0:
                            dfTemp['iso_value'][i] = float(0)
                        else:
                            dfTemp['iso_value'][i] = float((dfTemp['2b'][:i+1].sum() + (2 * dfTemp['3b'][:i+1].sum()) + (3 * dfTemp['hr'][:i+1].sum())) / dfTemp['ab'][:i+1].sum())
                        
                        dfTemp['iso_label'][i] = Format_Label(dfTemp['iso_value'][i])
                    df2 = pd.concat([df2, dfTemp]).reset_index(drop=True)
        df = df2
    else:
        for i in range(len(df)):
            if df['ab'][i] == 0:
                df['iso_value'][i] = float(0)
            else:
                df['iso_value'][i] = float((df['2b'][i] + (2 * df['3b'][i]) + (3 * df['hr'][i])) / df['ab'][i])
            
            df['iso_label'][i] = Format_Label(df['iso_value'][i])

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

def First_Latest_Appearance(df):
    if list(df.columns)[:2] == ['PlayerName', 'g'] or list(df.columns)[:2] == ['PlayerName', 'gs'] or list(df.columns)[:2] == ['PlayerName', 'FirstAppearance']:
        if 'FirstAppearance' not in df.columns:
            df.insert(1, 'FirstAppearance', '')

        if 'LatestAppearance' not in df.columns:
            df.insert(df.columns.get_loc('FirstAppearance')+1, 'LatestAppearance', '')

        for i in range(len(df['FirstAppearance'])):
            df1 = dfBatting_Gamelogs[dfBatting_Gamelogs['PlayerName'] == df['PlayerName'][i]].sort_values(['Year', 'Month', 'Day'], ascending=[True, True, True]).reset_index(drop=True)
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
            
            df1 = dfBatting_Gamelogs[dfBatting_Gamelogs['PlayerName'] == df['PlayerName'][i]].sort_values(['Year', 'Month', 'Day'], ascending=[False, False, False]).reset_index(drop=True)
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


dfBatting_Gamelogs = Def_DateString(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_PA(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_AVG(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_OBP(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_SLG(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_OPS(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_ISO(dfBatting_Gamelogs)
dfBatting_Gamelogs = Calc_MainPosition(dfBatting_Gamelogs)
dfBatting_Gamelogs = First_Latest_Appearance(dfBatting_Gamelogs)

dfBatting_Summary = Calc_PA(dfBatting_Summary)
dfBatting_Summary = Calc_AVG(dfBatting_Summary)
dfBatting_Summary = Calc_OBP(dfBatting_Summary)
dfBatting_Summary = Calc_SLG(dfBatting_Summary)
dfBatting_Summary = Calc_OPS(dfBatting_Summary)
dfBatting_Summary = Calc_ISO(dfBatting_Summary)
dfBatting_Summary = Calc_MainPosition(dfBatting_Summary)
dfBatting_Summary = First_Latest_Appearance(dfBatting_Summary)

dfBatting_Yearly = Calc_PA(dfBatting_Yearly)
dfBatting_Yearly = Calc_AVG(dfBatting_Yearly)
dfBatting_Yearly = Calc_OBP(dfBatting_Yearly)
dfBatting_Yearly = Calc_SLG(dfBatting_Yearly)
dfBatting_Yearly = Calc_OPS(dfBatting_Yearly)
dfBatting_Yearly = Calc_ISO(dfBatting_Yearly)
dfBatting_Yearly = Calc_MainPosition(dfBatting_Yearly)
dfBatting_Yearly = First_Latest_Appearance(dfBatting_Yearly)

dfBatting_Career = Calc_PA(dfBatting_Career)
dfBatting_Career = Calc_AVG(dfBatting_Career)
dfBatting_Career = Calc_OBP(dfBatting_Career)
dfBatting_Career = Calc_SLG(dfBatting_Career)
dfBatting_Career = Calc_OPS(dfBatting_Career)
dfBatting_Career = Calc_ISO(dfBatting_Career)
dfBatting_Career = Calc_MainPosition(dfBatting_Career)
dfBatting_Career = First_Latest_Appearance(dfBatting_Career)


dfBatting_Gamelogs.to_sql('db_Batting_Gamelogs', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfBatting_Summary.to_sql('db_Batting_Summary', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfBatting_Yearly.to_sql('db_Batting_Yearly', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)
dfBatting_Career.to_sql('db_Batting_Career', con=SQL_Engine, if_exists='replace', index=False, chunksize=1000)


filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Batting statistics calculated.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

