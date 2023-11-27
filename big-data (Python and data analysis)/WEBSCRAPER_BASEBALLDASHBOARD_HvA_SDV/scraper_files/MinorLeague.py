
import requests
import re
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime

Minor_IDs = (open("Data_retrieval/Results/MinorIDs.txt", "r")).readlines()
for i in range(len(Minor_IDs)):
    Minor_IDs[i] = (Minor_IDs[i])[:-1]

def Convert(string): 
    li = list(string.split("\n")) 
    return li

def ListToDF(cust_list):
    cust_list = [cust_list]
    cust_list = pd.DataFrame(cust_list)
    cust_list = cust_list.transpose()
    return cust_list

dfMinor_Pitching = pd.DataFrame()
dfMinor_Batting = pd.DataFrame()

# Scraping Minor League stats.
for Minor_ID in Minor_IDs:
    Minor_Seasons_URL = "https://www.baseball-reference.com/register/player.fcgi?id=" + Minor_ID
    Minor_Seasons_html = urlopen(Minor_Seasons_URL).read()
    Minor_Seasons_soup = soup(Minor_Seasons_html, "html.parser")
    InnerNav = str(Minor_Seasons_soup.findAll("div",{"id":"inner_nav"})[0])
    dfMinor_Seasons = InnerNav[InnerNav.find("Minors Game"):]

    #find the first p tag where the position is, "p" stands for paragraph 
    Position = Minor_Seasons_soup.find("p").text

    if "Pitcher" in Position:
        dfMinor_Seasons_Pitching = dfMinor_Seasons[dfMinor_Seasons.find('Pitching'):]
        dfMinor_Seasons_Pitching = dfMinor_Seasons_Pitching[dfMinor_Seasons_Pitching.find('<li>'):dfMinor_Seasons_Pitching.find('</ul>')]
        dfMinor_Seasons_Pitching = dfMinor_Seasons_Pitching.replace("</a></li>", "")
        dfMinor_Seasons_Pitching = Convert(dfMinor_Seasons_Pitching)[:-1]
        for i in range(len(dfMinor_Seasons_Pitching)):
            dfMinor_Seasons_Pitching[i] = (dfMinor_Seasons_Pitching[i])[(dfMinor_Seasons_Pitching[i]).rfind('>')+1:]

        dfMinor_Seasons_Batting = dfMinor_Seasons[dfMinor_Seasons.find('Batting'):]
        dfMinor_Seasons_Batting = dfMinor_Seasons_Batting[dfMinor_Seasons_Batting.find('<li>'):dfMinor_Seasons_Batting.find('</ul>')]
        dfMinor_Seasons_Batting = dfMinor_Seasons_Batting.replace("</a></li>", "")
        dfMinor_Seasons_Batting = Convert(dfMinor_Seasons_Batting)[:-1]
        for i in range(len(dfMinor_Seasons_Batting)):
            dfMinor_Seasons_Batting[i] = (dfMinor_Seasons_Batting[i])[(dfMinor_Seasons_Batting[i]).rfind('>')+1:]

    else:
        dfMinor_Seasons_Batting = dfMinor_Seasons[dfMinor_Seasons.find('<li>'):dfMinor_Seasons.find('</ul>')]
        dfMinor_Seasons_Batting = dfMinor_Seasons_Batting.replace("</a></li>", "")
        dfMinor_Seasons_Batting = Convert(dfMinor_Seasons_Batting)[:-1]
        for i in range(len(dfMinor_Seasons_Batting)):
            dfMinor_Seasons_Batting[i] = (dfMinor_Seasons_Batting[i])[(dfMinor_Seasons_Batting[i]).rfind('>')+1:]

    PlayerName = Minor_Seasons_soup.find("h1",{"itemprop":"name"}).text

    #scraping pitching stats if player is a pitcher 
    if "Pitcher" in Position:        
        for season in dfMinor_Seasons_Pitching:
            url = "https://www.baseball-reference.com/register/player.fcgi?id=" + Minor_ID + "&type=pgl&year=" + season
            Seasons_html = urlopen(url).read()
            
            Seasons_soup = soup(Seasons_html, "html.parser")
            dfMinor_Pitching_temp = Seasons_soup.findAll("table",{"id":"pitching_gamelogs_milb"})
            
            if len(dfMinor_Pitching_temp) > 0:
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[0]
                dfMinor_Pitching_temp = pd.read_html(str(dfMinor_Pitching_temp))[0]

                dfMinor_Pitching_temp.rename(columns={ dfMinor_Pitching_temp.columns[4]: "HomeGame"}, inplace=True)
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[dfMinor_Pitching_temp["H"] != "H"]
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[~dfMinor_Pitching_temp["Lev"].str.contains("Moved")]
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[dfMinor_Pitching_temp["Lev"] != "MLB-NL"] 
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[dfMinor_Pitching_temp["Lev"] != "MLB-AL"].reset_index(drop = True)
                ColumnsRemaining = ["Rk", "Date", "Lev", "Tm", "HomeGame", "Opp", "Inngs", "Dec", "IP", "H", "R", "ER", "BB", "SO", "HBP", "AB", "IBB", "BF", "FB", "GB", "Pit"]
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[ColumnsRemaining]

                #rename the columns 
                dfMinor_Pitching_temp.columns = ["MatchID", "Date", "League", "Team", "HomeGame", "Opponent", "gs", "Dec", "ip", "h", "r", "er", "bb", "so", "hbp", "ab", "ibb", "bf", "fo", "go", "np"]
            
                #inserting new column named "PlayerName" and "Year"
                dfMinor_Pitching_temp.insert(0, "PlayerName", PlayerName)
                dfMinor_Pitching_temp.insert(4, "Year", season)
                dfMinor_Pitching_temp.insert(5, "Month", season)
                dfMinor_Pitching_temp.insert(6, "Day", season)
                #converting the "Date" column to "Month" and "Day" which contains the month and day from the column "Date" and after that drop that column 
                for i in range(len(dfMinor_Pitching_temp["Date"])):
                    if "\xa0" in str((dfMinor_Pitching_temp["Date"])[i]):
                        (dfMinor_Pitching_temp["Date"])[i] = (dfMinor_Pitching_temp["Date"])[i].replace("\xa0", " ")
                    
                    if "(" in str((dfMinor_Pitching_temp["Date"])[i]):
                        (dfMinor_Pitching_temp["Date"])[i] = ((dfMinor_Pitching_temp["Date"])[i]).split("(")[0]

                    (dfMinor_Pitching_temp["Date"])[i] = str((dfMinor_Pitching_temp["Date"])[i]).strip()

                    DayMonthObj = datetime.strptime((dfMinor_Pitching_temp["Date"])[i], "%Y-%m-%d")
                    (dfMinor_Pitching_temp["Month"])[i] = DayMonthObj.strftime("%m")
                    (dfMinor_Pitching_temp["Day"])[i] = DayMonthObj.strftime("%d")

                dfMinor_Pitching_temp = dfMinor_Pitching_temp.drop(["Date"], axis=1)

                #convert HomeGame column to 1's for home games and 0's for away games(@ means away games)
                for i in range(len(dfMinor_Pitching_temp["HomeGame"])):
                    if (dfMinor_Pitching_temp["HomeGame"])[i] == "@":
                        (dfMinor_Pitching_temp["HomeGame"])[i] = 0
                    else:
                        (dfMinor_Pitching_temp["HomeGame"])[i] = 1
                
                for i in range(len(dfMinor_Pitching_temp["gs"])):
                    start = str(dfMinor_Pitching_temp["gs"][i])[:2]
                    if start == "GS" or start == "CG" or start == "1-":
                        dfMinor_Pitching_temp["gs"][i] = 1
                    else:
                        dfMinor_Pitching_temp["gs"][i] = 0

                #create three new columns -> "Win", "Loss", "Save" from "Dec" column then drop "Dec" column
                dfMinor_Pitching_temp["Win"] = [1 if x == "W" else 0 for x in dfMinor_Pitching_temp["Dec"]]
                dfMinor_Pitching_temp["Loss"] = [1 if x == "L" else 0 for x in dfMinor_Pitching_temp["Dec"]]
                dfMinor_Pitching_temp["Save"] = [1 if x == "S" else 0 for x in dfMinor_Pitching_temp["Dec"]]
                dfMinor_Pitching_temp = dfMinor_Pitching_temp.drop(["Dec"], axis=1)
                
                #arrange the columns so that it match the knbsb pitching dataframe  
                dfMinor_Pitching_temp = dfMinor_Pitching_temp[["PlayerName", "Team", "Opponent", "League", "HomeGame", "Year", "Month", "Day", "MatchID", "gs", "ip", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save"]]
                dfMinor_Pitching_temp.insert(4, "SeasonType", "Regular Season")

                dfMinor_Pitching = pd.concat([dfMinor_Pitching, dfMinor_Pitching_temp]).reset_index(drop=True)

                dfMinor_Pitching.dropna(subset=['Month'], how='all', inplace=True)            




    #scraping batting stats
    for season in dfMinor_Seasons_Batting:
        url = "https://www.baseball-reference.com/register/player.fcgi?id=" + Minor_ID + "&type=bgl&year=" + season
        Seasons_html = urlopen(url).read()
        Seasons_soup = soup(Seasons_html, "html.parser")
        
        dfMinor_Batting_temp = Seasons_soup.findAll("table",{"id":"batting_gamelogs_milb"})
        
        if len(dfMinor_Batting_temp) > 0:
            dfMinor_Batting_temp = dfMinor_Batting_temp[0]
            dfMinor_Batting_temp = pd.read_html(str(dfMinor_Batting_temp))[0]

            dfMinor_Batting_temp.rename(columns={ dfMinor_Batting_temp.columns[4]: "HomeGame" }, inplace = True)
            dfMinor_Batting_temp = dfMinor_Batting_temp[dfMinor_Batting_temp["PA"] != "PA"]
            dfMinor_Batting_temp = dfMinor_Batting_temp[~dfMinor_Batting_temp["Lev"].str.contains("Moved")]
            dfMinor_Batting_temp = dfMinor_Batting_temp[dfMinor_Batting_temp["Lev"] != "MLB-NL"] 
            dfMinor_Batting_temp = dfMinor_Batting_temp[dfMinor_Batting_temp["Lev"] != "MLB-AL"].reset_index(drop = True)
            ColsRemaining = ["Rk", "Date", "Lev", "Tm", "HomeGame", "Opp", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "HBP", "SH", "SF", "GDP", "SB", "CS", "Pos", "E"]
            dfMinor_Batting_temp = dfMinor_Batting_temp[ColsRemaining]

            # Rename column headers to match KNBSB data.
            dfMinor_Batting_temp.columns = ["MatchID", "Date", "League", "Team", "HomeGame", "Opponent", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "ibb", "so", "hbp", "sh", "sf", "gdp", "sb", "cs", "PositionString", "e"]

            dfMinor_Batting_temp.insert(0, "PlayerName", PlayerName)
            dfMinor_Batting_temp.insert(4, "Year", season)
            dfMinor_Batting_temp.insert(5, "Month", season)
            dfMinor_Batting_temp.insert(6, "Day", season)
            for i in range(len(dfMinor_Batting_temp["Date"])):
                if "\xa0" in str((dfMinor_Batting_temp["Date"])[i]):
                    (dfMinor_Batting_temp["Date"])[i] = (dfMinor_Batting_temp["Date"])[i].replace("\xa0", " ")
                
                if "(" in str((dfMinor_Batting_temp["Date"])[i]):
                    (dfMinor_Batting_temp["Date"])[i] = ((dfMinor_Batting_temp["Date"])[i]).split("(")[0]

                (dfMinor_Batting_temp["Date"])[i] = str((dfMinor_Batting_temp["Date"])[i]).strip()

                DayMonthObj = datetime.strptime((dfMinor_Batting_temp["Date"])[i], "%Y-%m-%d")
                (dfMinor_Batting_temp["Month"])[i] = DayMonthObj.strftime("%m")
                (dfMinor_Batting_temp["Day"])[i] = DayMonthObj.strftime("%d")

            dfMinor_Batting_temp = dfMinor_Batting_temp.drop(["Date"], axis=1)
            
            # Convert HomeGame column to 1's for home games and 0's for away games(@ means away games)
            for i in range(len(dfMinor_Batting_temp["HomeGame"])):
                if (dfMinor_Batting_temp["HomeGame"])[i] == "@":
                    (dfMinor_Batting_temp["HomeGame"])[i] = 0
                else:
                    (dfMinor_Batting_temp["HomeGame"])[i] = 1

            # Re-order columns to match KNBSB data.
            dfMinor_Batting_temp = dfMinor_Batting_temp[["PlayerName", "Team", "Opponent", "League", "HomeGame", "Year", "Month", "Day", "MatchID", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "gdp", "PositionString"]]

            # To add SeasonType
            dfMinor_Batting_temp.insert(4, "SeasonType", "Regular Season")      
            # Convert the Position_string to one-hot-encoding
            df1b = []
            df2b = []
            df3b = []
            dfc = []
            dfcf = []
            dfdh = []
            dflf = []
            dfp = []
            dfph = []
            dfpr = []
            dfrf = []
            dfss = []

            for RawPos in dfMinor_Batting_temp["PositionString"]:

                if " " in RawPos:
                    FirstPos = RawPos[:RawPos.find(" ")]
                    SecondPos = RawPos[RawPos.find(" ")+1:]
                else:
                    FirstPos = RawPos
                    SecondPos = ""

                if FirstPos == "1B" or SecondPos == "1B":
                    df1b.append(1)
                else:
                    df1b.append(0)

                if FirstPos == "2B" or SecondPos == "2B":
                    df2b.append(1)
                else:
                    df2b.append(0)

                if FirstPos == "3B" or SecondPos == "3B":
                    df3b.append(1)
                else:
                    df3b.append(0)

                if FirstPos == "C" or SecondPos == "C":
                    dfc.append(1)
                else:
                    dfc.append(0)

                if FirstPos == "CF" or SecondPos == "CF":
                    dfcf.append(1)
                else:
                    dfcf.append(0)

                if FirstPos == "DH" or SecondPos == "DH":
                    dfdh.append(1)
                else:
                    dfdh.append(0)

                if FirstPos == "LF" or SecondPos == "LF":
                    dflf.append(1)
                else:
                    dflf.append(0)

                if FirstPos == "P" or SecondPos == "P":
                    dfp.append(1)
                else:
                    dfp.append(0)

                if FirstPos == "PH" or SecondPos == "PH":
                    dfph.append(1)
                else:
                    dfph.append(0)

                if FirstPos == "PR" or SecondPos == "PR":
                    dfpr.append(1)
                else:
                    dfpr.append(0)

                if FirstPos == "RF" or SecondPos == "RF":
                    dfrf.append(1)
                else:
                    dfrf.append(0)

                if FirstPos == "SS" or SecondPos == "SS":
                    dfss.append(1)
                else:
                    dfss.append(0)

            df1b = [df1b]
            df1b = pd.DataFrame(df1b)
            df1b = df1b.transpose()

            df2b = [df2b]
            df2b = pd.DataFrame(df2b)
            df2b = df2b.transpose()

            df3b = [df3b]
            df3b = pd.DataFrame(df3b)
            df3b = df3b.transpose()

            dfc = [dfc]
            dfc = pd.DataFrame(dfc)
            dfc = dfc.transpose()

            dfcf = [dfcf]
            dfcf = pd.DataFrame(dfcf)
            dfcf = dfcf.transpose()

            dfdh = [dfdh]
            dfdh = pd.DataFrame(dfdh)
            dfdh = dfdh.transpose()

            dflf = [dflf]
            dflf = pd.DataFrame(dflf)
            dflf = dflf.transpose()

            dfp = [dfp]
            dfp = pd.DataFrame(dfp)
            dfp = dfp.transpose()

            dfph = [dfph]
            dfph = pd.DataFrame(dfph)
            dfph = dfph.transpose()

            dfpr = [dfpr]
            dfpr = pd.DataFrame(dfpr)
            dfpr = dfpr.transpose()

            dfrf = [dfrf]
            dfrf = pd.DataFrame(dfrf)
            dfrf = dfrf.transpose()

            dfss = [dfss]
            dfss = pd.DataFrame(dfss)
            dfss = dfss.transpose()

            dfPositions = pd.concat([df1b, df2b, df3b, dfc, dfcf, dfdh, dflf, dfp, dfph, dfpr, dfrf, dfss], axis=1)
            dfPositions.columns = ["Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss", ]

            dfMinor_Batting_temp = dfMinor_Batting_temp.drop(columns=["PositionString"])
            dfMinor_Batting_temp = pd.concat([dfMinor_Batting_temp, dfPositions], axis=1)

            # Merging the temporary DataFrame with the existing/main DataFrame
            dfMinor_Batting = pd.concat([dfMinor_Batting, dfMinor_Batting_temp]).reset_index(drop=True)
            dfMinor_Batting.dropna(subset=['Month'], how='all', inplace=True)


dfMinor_Pitching = dfMinor_Pitching.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)
dfMinor_Batting = dfMinor_Batting.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)


dfMinor_Pitching.to_csv("Data_retrieval/Results/Minor_Pitching.csv", index=False)
dfMinor_Batting.to_csv("Data_retrieval/Results/Minor_Batting.csv", index=False)


import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Minor League scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()


