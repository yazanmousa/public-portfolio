
import requests
import re
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime

Major_IDs = (open("Results/MajorIDs.txt", "r")).readlines()
for i in range(len(Major_IDs)):
    Major_IDs[i] = (Major_IDs[i])[:-1]

def Convert(string): 
    li = list(string.split("\n")) 
    return li

def ListToDF(cust_list):
    cust_list = [cust_list]
    cust_list = pd.DataFrame(cust_list)
    cust_list = cust_list.transpose()
    return cust_list

Postseason_list_Pitching = []
Postseason_list_Batting = []
Postseason_list_Fielding = []
dfMajor_Pitching = pd.DataFrame()
dfMajor_Batting = pd.DataFrame()
dfMajor_Fielding = pd.DataFrame()

for Major_ID in Major_IDs:
    Major_Seasons_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID
    Major_Seasons_html = urlopen(Major_Seasons_URL).read()
    Major_Seasons_soup = soup(Major_Seasons_html, "html.parser")
    InnerNav = str(Major_Seasons_soup.findAll("div",{"id":"inner_nav"})[0])
    dfMajor_Seasons = InnerNav[InnerNav.find('Game Logs'):]

    Position = Major_Seasons_soup.find("p").text

    if "Pitcher" in Position:
        dfMajor_Seasons_Pitching = dfMajor_Seasons[dfMajor_Seasons.find('<li>'):dfMajor_Seasons.find('</ul>')]
        dfMajor_Seasons_Pitching = dfMajor_Seasons_Pitching.replace("</a></li>", "")
        dfMajor_Seasons_Pitching = Convert(dfMajor_Seasons_Pitching)[:-1]
        for i in range(len(dfMajor_Seasons_Pitching)):
            dfMajor_Seasons_Pitching[i] = (dfMajor_Seasons_Pitching[i])[(dfMajor_Seasons_Pitching[i]).rfind('>')+1:]

        dfMajor_Seasons_Batting = dfMajor_Seasons[dfMajor_Seasons.find('Batting'):]
        dfMajor_Seasons_Batting = dfMajor_Seasons_Batting[dfMajor_Seasons_Batting.find('<li>'):dfMajor_Seasons_Batting.find('</ul>')]
        dfMajor_Seasons_Batting = dfMajor_Seasons_Batting.replace("</a></li>", "")
        dfMajor_Seasons_Batting = Convert(dfMajor_Seasons_Batting)[:-1]
        for i in range(len(dfMajor_Seasons_Batting)):
            dfMajor_Seasons_Batting[i] = (dfMajor_Seasons_Batting[i])[(dfMajor_Seasons_Batting[i]).rfind('>')+1:]

    else:
        dfMajor_Seasons_Batting = dfMajor_Seasons[dfMajor_Seasons.find('<li>'):dfMajor_Seasons.find('</ul>')]
        dfMajor_Seasons_Batting = dfMajor_Seasons_Batting.replace("</a></li>", "")
        dfMajor_Seasons_Batting = Convert(dfMajor_Seasons_Batting)[:-1]
        for i in range(len(dfMajor_Seasons_Batting)):
            dfMajor_Seasons_Batting[i] = (dfMajor_Seasons_Batting[i])[(dfMajor_Seasons_Batting[i]).rfind('>')+1:]

    dfMajor_Seasons_Fielding = dfMajor_Seasons[dfMajor_Seasons.find('Fielding'):]
    dfMajor_Seasons_Fielding = dfMajor_Seasons_Fielding[dfMajor_Seasons_Fielding.find('<li>'):dfMajor_Seasons_Fielding.find('</ul>')]
    dfMajor_Seasons_Fielding = dfMajor_Seasons_Fielding.replace("</a></li>", "")
    dfMajor_Seasons_Fielding = Convert(dfMajor_Seasons_Fielding)[:-1]
    for i in range(len(dfMajor_Seasons_Fielding)):
        dfMajor_Seasons_Fielding[i] = (dfMajor_Seasons_Fielding[i])[(dfMajor_Seasons_Fielding[i]).rfind('>')+1:]

    if "Pitcher" in Position and "Postseason" in dfMajor_Seasons_Pitching:
        Postseason_list_Pitching.append(Major_ID)
        dfMajor_Seasons_Pitching = list(filter(lambda a: a != "Postseason", dfMajor_Seasons_Pitching))

    if "Postseason" in dfMajor_Seasons_Batting:
        Postseason_list_Batting.append(Major_ID)
        dfMajor_Seasons_Batting = list(filter(lambda a: a != "Postseason", dfMajor_Seasons_Batting))

    if "Postseason" in dfMajor_Seasons_Fielding:
        Postseason_list_Fielding.append(Major_ID)
        dfMajor_Seasons_Fielding = list(filter(lambda a: a != "Postseason", dfMajor_Seasons_Fielding))

    PlayerName = Major_Seasons_soup.find("h1",{"itemprop":"name"}).text

    # Scraping Pitching stats (if player is Pitcher).
    if "Pitcher" in Position:
        for Year in dfMajor_Seasons_Pitching: 
            Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=p&year=" + Year
            Season_html = urlopen(Season_URL).read()
            Season_soup = soup(Season_html, "html.parser")
            dfMajor_Pitching_temp = Season_soup.findAll("table",{"id":"pitching_gamelogs"})[0]
            dfMajor_Pitching_temp = pd.read_html(str(dfMajor_Pitching_temp))[0]
            dfMajor_Pitching_temp.rename(columns={ dfMajor_Pitching_temp.columns[5]: "HomeGame" }, inplace = True)
            dfMajor_Pitching_temp = dfMajor_Pitching_temp[dfMajor_Pitching_temp["Rslt"] != "Rslt"]
            dfMajor_Pitching_temp = dfMajor_Pitching_temp.dropna(subset=["Date"]).reset_index(drop=True)
            ColsRemaining = ["Gtm", "Date", "Tm", "HomeGame", "Opp", "Inngs", "Dec", "IP", "H", "R", "ER", "BB", "SO", "HBP", "IBB", "AB", "BF", "FB", "GB", "Pit"]
            dfMajor_Pitching_temp = dfMajor_Pitching_temp[ColsRemaining]

            dfMajor_Pitching_temp.columns = ["MatchID", "Date", "Team", "HomeGame", "Opponent", "gs", "Dec", "ip", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np"]

            dfMajor_Pitching_temp.insert(0, "PlayerName", PlayerName)
            dfMajor_Pitching_temp.insert(3, "Year", Year)
            dfMajor_Pitching_temp.insert(4, "Month", "")
            dfMajor_Pitching_temp.insert(5, "Day", "")

            # Cleaning the MatchID column (removing parentheses etc.)
            for i in range(len(dfMajor_Pitching_temp["MatchID"])):
                if "(" in str((dfMajor_Pitching_temp["MatchID"])[i]):
                    (dfMajor_Pitching_temp["MatchID"])[i] = ((dfMajor_Pitching_temp["MatchID"])[i])[:((dfMajor_Pitching_temp["MatchID"])[i]).find("(")-1]

            # Convert Date-values to numbers in separate columns.
            for i in range(len(dfMajor_Pitching_temp["Date"])):
                if "\xa0" in str((dfMajor_Pitching_temp["Date"])[i]):
                    (dfMajor_Pitching_temp["Date"])[i] = (dfMajor_Pitching_temp["Date"])[i].replace("\xa0", " ")
                
                if "(" in str((dfMajor_Pitching_temp["Date"])[i]):
                    (dfMajor_Pitching_temp["Date"])[i] = ((dfMajor_Pitching_temp["Date"])[i]).split("(")[0]

                if len(str((dfMajor_Pitching_temp["Date"])[i])) > 6:
                    (dfMajor_Pitching_temp["Date"])[i] = ((dfMajor_Pitching_temp["Date"])[i])[:6]

                (dfMajor_Pitching_temp["Date"])[i] = str((dfMajor_Pitching_temp["Date"])[i]).strip()

                DayMonthObj = datetime.strptime((dfMajor_Pitching_temp["Date"])[i], "%b %d")
                (dfMajor_Pitching_temp["Month"])[i] = DayMonthObj.strftime("%m")
                (dfMajor_Pitching_temp["Day"])[i] = DayMonthObj.strftime("%d")

            dfMajor_Pitching_temp = dfMajor_Pitching_temp.drop(["Date"], axis=1)

            # Convert HomeGame column to 1's for home games and 0's for away games
            for i in range(len(dfMajor_Pitching_temp["HomeGame"])):
                if (dfMajor_Pitching_temp["HomeGame"])[i] == "@":
                    (dfMajor_Pitching_temp["HomeGame"])[i] = 0
                else:
                    (dfMajor_Pitching_temp["HomeGame"])[i] = 1

            # Convert the Team and Opponent IDs to full team names.
            try:
                dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
            except:
                dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
            dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]

            if int(Year) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int(Year)

            dfTeamNames = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            for i in range(len(dfMajor_Pitching_temp["Team"])):
                TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Pitching_temp["Team"])[i]]
                (dfMajor_Pitching_temp["Team"])[i] = (list(TeamRow["name"]))[0]

            for i in range(len(dfMajor_Pitching_temp["Opponent"])):
                TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Pitching_temp["Opponent"])[i]]
                try:
                    (dfMajor_Pitching_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]    
                except:
                    print((dfMajor_Pitching_temp["Opponent"])[i])
                    print(list(TeamRow["name"]))

            dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Win", 0)
            dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Loss", 0)
            dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Save", 0)

            for i in range(len(dfMajor_Pitching_temp["gs"])):
                start = str(dfMajor_Pitching_temp["gs"][i])[:2]
                if start == "GS" or start == "CG" or start == "1-":
                    dfMajor_Pitching_temp["gs"][i] = 1
                else:
                    dfMajor_Pitching_temp["gs"][i] = 0

            for i in range(len(dfMajor_Pitching_temp["Dec"])):
                decision = str(dfMajor_Pitching_temp["Dec"][i])
                if decision != "":
                    decision = decision.split("(")[0]
                    if decision == "W":
                        win = 1
                        dfMajor_Pitching_temp["Win"][i] = win
                    if decision == "L":
                        loss = 1
                        dfMajor_Pitching_temp["Loss"][i] = loss
                    if decision == "S":
                        save = 1
                        dfMajor_Pitching_temp["Save"][i] = save
            
            dfMajor_Pitching_temp = dfMajor_Pitching_temp.drop(["Dec"], axis=1)

            dfMajor_Pitching_temp = dfMajor_Pitching_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "gs", "ip", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save"]]

            dfMajor_Pitching_temp.insert(3, "League", "MLB (USA)")
            dfMajor_Pitching_temp.insert(4, "SeasonType", "Regular Season")

            dfMajor_Pitching = pd.concat([dfMajor_Pitching, dfMajor_Pitching_temp]).reset_index(drop=True)


    # Scraping Batting stats.
    for Year in dfMajor_Seasons_Batting:
        Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=b&year=" + Year
        Season_html = urlopen(Season_URL).read()
        Season_soup = soup(Season_html, "html.parser")
        dfMajor_Batting_temp = Season_soup.findAll("table",{"id":"batting_gamelogs"})[0]
        dfMajor_Batting_temp = pd.read_html(str(dfMajor_Batting_temp))[0]
        dfMajor_Batting_temp.rename(columns={ dfMajor_Batting_temp.columns[5]: "HomeGame" }, inplace = True)
        dfMajor_Batting_temp = dfMajor_Batting_temp[dfMajor_Batting_temp["Rslt"] != "Rslt"]
        dfMajor_Batting_temp = dfMajor_Batting_temp.dropna(subset=["Date"]).reset_index(drop=True)
        ColsRemaining = ["Gtm", "Date", "Tm", "HomeGame", "Opp", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "HBP", "SH", "SF", "GDP", "SB", "CS", "Pos"]
        dfMajor_Batting_temp = dfMajor_Batting_temp[ColsRemaining]

        # Rename column headers to match KNBSB data.
        dfMajor_Batting_temp.columns = ["MatchID", "Date", "Team", "HomeGame", "Opponent", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "ibb", "so", "hbp", "sh", "sf", "gdp", "sb", "cs", "PositionString"]


        dfMajor_Batting_temp.insert(0, "PlayerName", PlayerName)
        dfMajor_Batting_temp.insert(4, "Year", Year)
        dfMajor_Batting_temp.insert(5, "Month", "")
        dfMajor_Batting_temp.insert(6, "Day", "")

        # Cleaning the MatchID column (removing parentheses etc.)
        for i in range(len(dfMajor_Batting_temp["MatchID"])):
            if "(" in str((dfMajor_Batting_temp["MatchID"])[i]):
                (dfMajor_Batting_temp["MatchID"])[i] = ((dfMajor_Batting_temp["MatchID"])[i])[:((dfMajor_Batting_temp["MatchID"])[i]).find("(")-1]

        # Convert Date-values to numbers in separate columns.
        for i in range(len(dfMajor_Batting_temp["Date"])):
            if "\xa0" in str((dfMajor_Batting_temp["Date"])[i]):
                (dfMajor_Batting_temp["Date"])[i] = (dfMajor_Batting_temp["Date"])[i].replace("\xa0", " ")
            
            if len(str((dfMajor_Batting_temp["Date"])[i])) > 6:
                (dfMajor_Batting_temp["Date"])[i] = ((dfMajor_Batting_temp["Date"])[i])[:6]

            (dfMajor_Batting_temp["Date"])[i] = str((dfMajor_Batting_temp["Date"])[i]).strip()

            DayMonthObj = datetime.strptime((dfMajor_Batting_temp["Date"])[i], "%b %d")
            (dfMajor_Batting_temp["Month"])[i] = DayMonthObj.strftime("%m")
            (dfMajor_Batting_temp["Day"])[i] = DayMonthObj.strftime("%d")

        dfMajor_Batting_temp = dfMajor_Batting_temp.drop(["Date"], axis=1)

        # Convert HomeGame column to 1's for home games and 0's for away games
        for i in range(len(dfMajor_Batting_temp["HomeGame"])):
            if (dfMajor_Batting_temp["HomeGame"])[i] == "@":
                (dfMajor_Batting_temp["HomeGame"])[i] = 0
            else:
                (dfMajor_Batting_temp["HomeGame"])[i] = 1

        # Convert the Team and Opponent IDs to full team names.
        try:
            dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
        except:
            dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
        dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]
        TeamNames_year = max(list(dfTeamNames['yearID']))

        if int(Year) > TeamNames_year:
            TeamNames_yearnumber = TeamNames_year
        else:
            TeamNames_yearnumber = int(Year)

        dfTeamNames = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

        for i in range(len(dfMajor_Batting_temp["Team"])):
            TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Batting_temp["Team"])[i]]
            (dfMajor_Batting_temp["Team"])[i] = (list(TeamRow["name"]))[0]

        for i in range(len(dfMajor_Batting_temp["Opponent"])):
            TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Batting_temp["Opponent"])[i]]
            (dfMajor_Batting_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]

        # Re-order columns to match KNBSB data.
        dfMajor_Batting_temp = dfMajor_Batting_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "gdp", "PositionString"]]

        # To add: League, SeasonType
        dfMajor_Batting_temp.insert(3, "League", "MLB (USA)")
        dfMajor_Batting_temp.insert(4, "SeasonType", "Regular Season")

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

        for RawPos in dfMajor_Batting_temp["PositionString"]:
            RawPos = str(RawPos)
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

        dfMajor_Batting_temp = dfMajor_Batting_temp.drop(columns=["PositionString"]).reset_index(drop=True)
        dfMajor_Batting_temp = pd.concat([dfMajor_Batting_temp, dfPositions], axis=1)

        # Merging the temporary DataFrame with the existing/main DataFrame
        dfMajor_Batting = pd.concat([dfMajor_Batting, dfMajor_Batting_temp]).reset_index(drop=True)


    # Scraping Fielding stats.
    for Year in dfMajor_Seasons_Fielding:
        Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=f&year=" + Year
        Season_html = urlopen(Season_URL).read()
        Season_soup = soup(Season_html, "html.parser")
        dfMajor_Fielding_temp = Season_soup.findAll("table")[0]
        dfMajor_Fielding_temp = pd.read_html(str(dfMajor_Fielding_temp))[0]
        dfMajor_Fielding_temp.rename(columns={ dfMajor_Fielding_temp.columns[4]: "HomeGame" }, inplace = True)
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[dfMajor_Fielding_temp["Rslt"] != "Rslt"]
        dfMajor_Fielding_temp = dfMajor_Fielding_temp.dropna(subset=["Gtm"]).reset_index(drop=True)
        ColsRemaining = ["Gtm", "Date", "Tm", "HomeGame", "Opp", "BF", "Inn", "PO", "A", "E", "Ch", "DP", "Pos"]
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[ColsRemaining]

        # Rename column headers to match KNBSB data.
        dfMajor_Fielding_temp.columns = ["MatchID", "Date", "Team", "HomeGame", "Opponent", "BatrsFaced", "Inngs", "po", "a", "e", "DefChances", "DP_turned", "PositionString"]


        dfMajor_Fielding_temp.insert(0, "PlayerName", PlayerName)
        dfMajor_Fielding_temp.insert(3, "Year", Year)
        dfMajor_Fielding_temp.insert(4, "Month", "")
        dfMajor_Fielding_temp.insert(5, "Day", "")

        # Cleaning the MatchID column (removing parentheses etc.)
        for i in range(len(dfMajor_Fielding_temp["MatchID"])):
            if "(" in str((dfMajor_Fielding_temp["MatchID"])[i]):
                (dfMajor_Fielding_temp["MatchID"])[i] = ((dfMajor_Fielding_temp["MatchID"])[i])[:((dfMajor_Fielding_temp["MatchID"])[i]).find("(")-1]

        # Convert Date-values to numbers in separate columns.
        for i in range(len(dfMajor_Fielding_temp["Date"])):
            if "\xa0" in str((dfMajor_Fielding_temp["Date"])[i]):
                (dfMajor_Fielding_temp["Date"])[i] = (dfMajor_Fielding_temp["Date"])[i].replace("\xa0", " ")
            
            if len(str((dfMajor_Fielding_temp["Date"])[i])) > 6:
                (dfMajor_Fielding_temp["Date"])[i] = ((dfMajor_Fielding_temp["Date"])[i])[:6]

            (dfMajor_Fielding_temp["Date"])[i] = str((dfMajor_Fielding_temp["Date"])[i]).strip()

            DayMonthObj = datetime.strptime((dfMajor_Fielding_temp["Date"])[i], "%b %d")
            (dfMajor_Fielding_temp["Month"])[i] = DayMonthObj.strftime("%m")
            (dfMajor_Fielding_temp["Day"])[i] = DayMonthObj.strftime("%d")

        dfMajor_Fielding_temp = dfMajor_Fielding_temp.drop(["Date"], axis=1)

        # Convert HomeGame column to 1's for home games and 0's for away games
        for i in range(len(dfMajor_Fielding_temp["HomeGame"])):
            if (dfMajor_Fielding_temp["HomeGame"])[i] == "@":
                (dfMajor_Fielding_temp["HomeGame"])[i] = 0
            else:
                (dfMajor_Fielding_temp["HomeGame"])[i] = 1

        # Convert the Team and Opponent IDs to full team names.
        try:
            dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
        except:
            dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
        dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]
        TeamNames_year = max(list(dfTeamNames['yearID']))

        if int(Year) > TeamNames_year:
            TeamNames_yearnumber = TeamNames_year
        else:
            TeamNames_yearnumber = int(Year)
        
        dfTeamNames = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

        for i in range(len(dfMajor_Fielding_temp["Team"])):
            TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Fielding_temp["Team"])[i]]
            (dfMajor_Fielding_temp["Team"])[i] = (list(TeamRow["name"]))[0]

        for i in range(len(dfMajor_Fielding_temp["Opponent"])):
            TeamRow = dfTeamNames[dfTeamNames["teamIDBR"] == (dfMajor_Fielding_temp["Opponent"])[i]]
            (dfMajor_Fielding_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]

        # Re-order columns to match KNBSB data.
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "po", "a", "e", "PositionString"]]

        # To add: League, SeasonType
        dfMajor_Fielding_temp.insert(3, "League", "MLB (USA)")
        dfMajor_Fielding_temp.insert(4, "SeasonType", "Regular Season")

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

        for RawPos in dfMajor_Fielding_temp["PositionString"]:
            RawPos = str(RawPos)
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

        dfMajor_Fielding_temp = dfMajor_Fielding_temp.drop(columns=["PositionString"]).reset_index(drop=True)
        dfMajor_Fielding_temp = pd.concat([dfMajor_Fielding_temp, dfPositions], axis=1)

        # Merging the temporary DataFrame with the existing/main DataFrame
        dfMajor_Fielding = pd.concat([dfMajor_Fielding, dfMajor_Fielding_temp]).reset_index(drop=True)


#------------ POSTSEASON SCRAPING ------------
for Major_ID in Postseason_list_Pitching[:1]:
    Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=p&year=0&post=1" 
    Season_html = urlopen(Season_URL).read()
    Season_soup = soup(Season_html, "html.parser")
    table = Season_soup.findAll("table",{"id":"pitching_gamelogs_post"})
    
    for dfMajor_Pitching_temp in table: 
        dfMajor_Pitching_temp = pd.read_html(str(dfMajor_Pitching_temp))[0]
        dfMajor_Pitching_temp.rename(columns={ dfMajor_Pitching_temp.columns[5]: "HomeGame" }, inplace = True)
        dfMajor_Pitching_temp = dfMajor_Pitching_temp[dfMajor_Pitching_temp["Rslt"] != "Rslt"]
        dfMajor_Pitching_temp = dfMajor_Pitching_temp.dropna(subset=["Rslt"]).reset_index(drop=True)
        PlayerName = Season_soup.find("h1",{"itemprop":"name"}).text

        ColsRemaining = ["Rk","Year","Date", "Tm", "HomeGame", "Opp", "Inngs", "Dec", "AB", "IP", "BF", "R", "ER", "H", "BB", "IBB", "SO", "HBP", "FB", "GB", "Pit"]

        dfMajor_Pitching_temp = dfMajor_Pitching_temp[ColsRemaining]

        # Rename column headers to match KNBSB data.
        dfMajor_Pitching_temp.drop = ["2b", "3b", "hr", "rbi", "sh", "sf", "gdp", "sb", "cs", "PositionString"]
        dfMajor_Pitching_temp.columns = ["MatchID", "Year", "Date", "Team", "HomeGame", "Opponent", "gs", "Dec", "ab", "ip", "bf", "r", "er", "h", "bb", "ibb", "so", "hbp", "fo", "go", "np"]

        dfMajor_Pitching_temp.insert(0, "PlayerName", PlayerName)
        dfMajor_Pitching_temp.insert(7, "Month", "")
        dfMajor_Pitching_temp.insert(8, "Day", "")


        # Cleaning the MatchID column (removing parentheses etc.)
        for i in range(len(dfMajor_Pitching_temp["MatchID"])):
            if "(" in str((dfMajor_Pitching_temp["MatchID"])[i]):
                (dfMajor_Pitching_temp["MatchID"])[i] = ((dfMajor_Pitching_temp["MatchID"])[i])[:((dfMajor_Pitching_temp["MatchID"])[i]).find("(")-1]

        # Convert Date-values to numbers in separate columns.
        for i in range(len(dfMajor_Pitching_temp["Date"])):
            if "\xa0" in str((dfMajor_Pitching_temp["Date"])[i]):
                (dfMajor_Pitching_temp["Date"])[i] = (dfMajor_Pitching_temp["Date"])[i].replace("\xa0", " ")
            
            if len(str((dfMajor_Pitching_temp["Date"])[i])) > 6:
                (dfMajor_Pitching_temp["Date"])[i] = ((dfMajor_Pitching_temp["Date"])[i])[:6]

            (dfMajor_Pitching_temp["Date"])[i] = str((dfMajor_Pitching_temp["Date"])[i]).strip()

            DayMonthObj = datetime.strptime((dfMajor_Pitching_temp["Date"])[i], "%b %d")
            (dfMajor_Pitching_temp["Month"])[i] = DayMonthObj.strftime("%m")
            (dfMajor_Pitching_temp["Day"])[i] = DayMonthObj.strftime("%d")

        #dfMajor_Pitching_temp = dfMajor_Pitching_temp.drop(["Date"], axis=1)

        # Convert HomeGame column to 1's for home games and 0's for away games
        for i in range(len(dfMajor_Pitching_temp["HomeGame"])):
            if (dfMajor_Pitching_temp["HomeGame"])[i] == "@":
                (dfMajor_Pitching_temp["HomeGame"])[i] = 0
            else:
                (dfMajor_Pitching_temp["HomeGame"])[i] = 1

        # Convert the Team and Opponent IDs to full team names.
        try:
            dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
        except:
            dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
        dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]

        for i in range(len(dfMajor_Pitching_temp["Team"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Pitching_temp["Team"])[i]]
            (dfMajor_Pitching_temp["Team"])[i] = (list(TeamRow["name"]))[0]

        for i in range(len(dfMajor_Pitching_temp["Opponent"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = (dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Pitching_temp["Opponent"])[i]])
            (dfMajor_Pitching_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]

        # Re-order columns to match KNBSB data.
        dfMajor_Pitching_temp = dfMajor_Pitching_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "gs", "ip", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Dec"]]

        # To add: League, SeasonType
        dfMajor_Pitching_temp.insert(3, "League", "MLB (USA)")
        dfMajor_Pitching_temp.insert(4, "SeasonType", "Post-Season")

        #Remove parentheses  
        dfMajor_Pitching_temp["Dec"] = dfMajor_Pitching_temp['Dec'].str.replace(r"\(.*\)","")

        # Convert the Dec to one-hot-encoding
        dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Win", 0)
        dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Loss", 0)
        dfMajor_Pitching_temp.insert(len(dfMajor_Pitching_temp.columns), "Save", 0)

        for i in range(len(dfMajor_Pitching_temp["gs"])):
            start = str(dfMajor_Pitching_temp["gs"][i])[:2]
            if start == "GS" or start == "CG" or start == "1-":
                dfMajor_Pitching_temp["gs"][i] = 1
            else:
                dfMajor_Pitching_temp["gs"][i] = 0

        for i in range(len(dfMajor_Pitching_temp["Dec"])):
            decision = str(dfMajor_Pitching_temp["Dec"][i])
            if decision != "":
                decision = decision.split("(")[0]
                if decision == "W":
                    win = 1
                    dfMajor_Pitching_temp["Win"][i] = win
                if decision == "L":
                    loss = 1
                    dfMajor_Pitching_temp["Loss"][i] = loss
                if decision == "S":
                    save = 1
                    dfMajor_Pitching_temp["Save"][i] = save
        
        dfMajor_Pitching_temp = dfMajor_Pitching_temp.drop(["Dec"], axis=1)

        # Merging the temporary DataFrame with the existing/main DataFrame
        dfMajor_Pitching = pd.concat([dfMajor_Pitching, dfMajor_Pitching_temp]).reset_index(drop=True)



for Major_ID in Postseason_list_Batting: 
    Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=b&year=0&post=1" 
    Season_html = urlopen(Season_URL).read()
    Season_soup = soup(Season_html, "html.parser")
    table = Season_soup.findAll("table",{"id":"batting_gamelogs_post"})
    
    for dfMajor_Batting_temp in table: 
        dfMajor_Batting_temp = pd.read_html(str(dfMajor_Batting_temp))[0]
        dfMajor_Batting_temp.rename(columns={ dfMajor_Batting_temp.columns[5]: "HomeGame" }, inplace = True)
        dfMajor_Batting_temp = dfMajor_Batting_temp[dfMajor_Batting_temp["Rslt"] != "Rslt"]
        dfMajor_Batting_temp = dfMajor_Batting_temp.dropna(subset=["Rslt"]).reset_index(drop=True)
        PlayerName = Season_soup.find("h1",{"itemprop":"name"}).text


        ColsRemaining = ["Rk","Year","Date", "Tm", "HomeGame", "Opp", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "HBP", "SH", "SF", "GDP", "SB", "CS", "Pos"]
        dfMajor_Batting_temp = dfMajor_Batting_temp[ColsRemaining]

        # Rename column headers to match KNBSB data.
        dfMajor_Batting_temp.columns = ["MatchID", "Year", "Date", "Team", "HomeGame", "Opponent", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "ibb", "so", "hbp", "sh", "sf", "gdp", "sb", "cs", "PositionString"]


        dfMajor_Batting_temp.insert(0, "PlayerName", PlayerName)
        dfMajor_Batting_temp.insert(4, "Month", "")
        dfMajor_Batting_temp.insert(5, "Day", "")

        # Cleaning the MatchID column (removing parentheses etc.)
        for i in range(len(dfMajor_Batting_temp["MatchID"])):
            if "(" in str((dfMajor_Batting_temp["MatchID"])[i]):
                (dfMajor_Batting_temp["MatchID"])[i] = ((dfMajor_Batting_temp["MatchID"])[i])[:((dfMajor_Batting_temp["MatchID"])[i]).find("(")-1]

        # Convert Date-values to numbers in separate columns.
        for i in range(len(dfMajor_Batting_temp["Date"])):
            if "\xa0" in str((dfMajor_Batting_temp["Date"])[i]):
                (dfMajor_Batting_temp["Date"])[i] = (dfMajor_Batting_temp["Date"])[i].replace("\xa0", " ")
            
            if len(str((dfMajor_Batting_temp["Date"])[i])) > 6:
                (dfMajor_Batting_temp["Date"])[i] = ((dfMajor_Batting_temp["Date"])[i])[:6]

            (dfMajor_Batting_temp["Date"])[i] = str((dfMajor_Batting_temp["Date"])[i]).strip()

            DayMonthObj = datetime.strptime((dfMajor_Batting_temp["Date"])[i], "%b %d")
            (dfMajor_Batting_temp["Month"])[i] = DayMonthObj.strftime("%m")
            (dfMajor_Batting_temp["Day"])[i] = DayMonthObj.strftime("%d")

        dfMajor_Batting_temp = dfMajor_Batting_temp.drop(["Date"], axis=1)

        # Convert HomeGame column to 1's for home games and 0's for away games
        for i in range(len(dfMajor_Batting_temp["HomeGame"])):
            if (dfMajor_Batting_temp["HomeGame"])[i] == "@":
                (dfMajor_Batting_temp["HomeGame"])[i] = 0
            else:
                (dfMajor_Batting_temp["HomeGame"])[i] = 1

        # Convert the Team and Opponent IDs to full team names.
        try:
            dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
        except:
            dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
        dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]

        for i in range(len(dfMajor_Batting_temp["Team"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Batting_temp["Team"])[i]]
            (dfMajor_Batting_temp["Team"])[i] = (list(TeamRow["name"]))[0]

        for i in range(len(dfMajor_Batting_temp["Opponent"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = (dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Batting_temp["Opponent"])[i]])
            (dfMajor_Batting_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]

        # Re-order columns to match KNBSB data.
        dfMajor_Batting_temp = dfMajor_Batting_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "gdp", "PositionString"]]

        # To add: League, SeasonType
        dfMajor_Batting_temp.insert(3, "League", "MLB (USA)")
        dfMajor_Batting_temp.insert(4, "SeasonType", "Post-Season")

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

        for RawPos in dfMajor_Batting_temp["PositionString"]:
            RawPos = str(RawPos)
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

        dfMajor_Batting_temp = dfMajor_Batting_temp.drop(columns=["PositionString"]).reset_index(drop=True)
        dfMajor_Batting_temp = pd.concat([dfMajor_Batting_temp, dfPositions], axis=1)

        # Merging the temporary DataFrame with the existing/main DataFrame
        dfMajor_Batting = pd.concat([dfMajor_Batting, dfMajor_Batting_temp]).reset_index(drop=True)


for Major_ID in Postseason_list_Fielding: 
    Season_URL = "https://www.baseball-reference.com/players/gl.fcgi?id=" + Major_ID + "&t=f&year=0&post=1" 
    Season_html = urlopen(Season_URL).read()
    Season_soup = soup(Season_html, "html.parser")
    Season_string = str(Season_soup)
    NoOfTables = Season_string.count('<table class="sortable stats_table"')

    Test = Season_string[Season_string.find('caption'):]

    for i in range(NoOfTables):
        dfMajor_Fielding_temp = Season_string[Season_string.find('<table class="sortable stats_table"'):]
        
        if i > 0:
            for x in range(i):
                dfMajor_Fielding_temp = dfMajor_Fielding_temp[1:]
                dfMajor_Fielding_temp = dfMajor_Fielding_temp[dfMajor_Fielding_temp.find('<table class="sortable stats_table"'):]
        
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[:dfMajor_Fielding_temp.find('</table>')+8]
        Position = dfMajor_Fielding_temp[dfMajor_Fielding_temp.find('<caption>')+9:dfMajor_Fielding_temp.find('</caption>')]
        Position = Position[Position.find('(as ')+4:Position.find(')')]
        dfMajor_Fielding_temp = pd.read_html(dfMajor_Fielding_temp)[0]

        if len(dfMajor_Fielding_temp.columns) == 16:
            dfMajor_Fielding_temp.columns = ["Rk","Year","Series", "Date", "Tm", "HomeGame", "Opp", "Rslt", "Inngs", "BF", "Inn", "PO", "A", "E", "Ch", "DP"]
        elif len(dfMajor_Fielding_temp.columns) == 19:
            dfMajor_Fielding_temp.columns = ["Rk","Year","Series", "Date", "Tm", "HomeGame", "Opp", "Rslt", "Inngs", "BF", "Inn", "PO", "A", "E", "Ch", "DP", "SB", "CS", "PO2"]
            dfMajor_Fielding_temp = dfMajor_Fielding_temp[["Rk","Year","Series", "Date", "Tm", "HomeGame", "Opp", "Rslt", "Inngs", "BF", "Inn", "PO", "A", "E", "Ch", "DP"]]

        dfMajor_Fielding_temp = dfMajor_Fielding_temp[dfMajor_Fielding_temp["Rslt"] != "Rslt"]
        dfMajor_Fielding_temp = dfMajor_Fielding_temp.dropna(subset=["Rslt"]).reset_index(drop=True)
        PlayerName = Season_soup.find("h1",{"itemprop":"name"}).text


        ColsRemaining = ["Rk", "Year", "Date", "Tm", "HomeGame", "Opp", "PO", "A", "E"]
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[ColsRemaining]

        # Rename column headers to match KNBSB data.
        dfMajor_Fielding_temp.columns = ["MatchID", "Year", "Date", "Team", "HomeGame", "Opponent", "po", "a", "e"]


        dfMajor_Fielding_temp.insert(0, "PlayerName", PlayerName)
        dfMajor_Fielding_temp.insert(4, "Month", "")
        dfMajor_Fielding_temp.insert(5, "Day", "")
        dfMajor_Fielding_temp.insert(12, "PositionString", Position)

        # Cleaning the MatchID column (removing parentheses etc.)
        for i in range(len(dfMajor_Fielding_temp["MatchID"])):
            if "(" in str((dfMajor_Fielding_temp["MatchID"])[i]):
                (dfMajor_Fielding_temp["MatchID"])[i] = ((dfMajor_Fielding_temp["MatchID"])[i])[:((dfMajor_Fielding_temp["MatchID"])[i]).find("(")-1]

        # Convert Date-values to numbers in separate columns.
        for i in range(len(dfMajor_Fielding_temp["Date"])):
            if "\xa0" in str((dfMajor_Fielding_temp["Date"])[i]):
                (dfMajor_Fielding_temp["Date"])[i] = (dfMajor_Fielding_temp["Date"])[i].replace("\xa0", " ")
            
            if len(str((dfMajor_Fielding_temp["Date"])[i])) > 6:
                (dfMajor_Fielding_temp["Date"])[i] = ((dfMajor_Fielding_temp["Date"])[i])[:6]

            (dfMajor_Fielding_temp["Date"])[i] = str((dfMajor_Fielding_temp["Date"])[i]).strip()

            DayMonthObj = datetime.strptime((dfMajor_Fielding_temp["Date"])[i], "%b %d")
            (dfMajor_Fielding_temp["Month"])[i] = DayMonthObj.strftime("%m")
            (dfMajor_Fielding_temp["Day"])[i] = DayMonthObj.strftime("%d")

        dfMajor_Fielding_temp = dfMajor_Fielding_temp.drop(["Date"], axis=1)

        # Convert HomeGame column to 1's for home games and 0's for away games
        for i in range(len(dfMajor_Fielding_temp["HomeGame"])):
            if (dfMajor_Fielding_temp["HomeGame"])[i] == "@":
                (dfMajor_Fielding_temp["HomeGame"])[i] = 0
            else:
                (dfMajor_Fielding_temp["HomeGame"])[i] = 1

        # Convert the Team and Opponent IDs to full team names.
        try:
            dfTeamNames = pd.read_csv("https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/Teams.csv")
        except:
            dfTeamNames = pd.read_csv("Necessities/MLB_Teams.csv")
        dfTeamNames = dfTeamNames[["yearID", "name", "teamIDBR"]]

        for i in range(len(dfMajor_Fielding_temp["Team"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Fielding_temp["Team"])[i]]
            (dfMajor_Fielding_temp["Team"])[i] = (list(TeamRow["name"]))[0]

        for i in range(len(dfMajor_Fielding_temp["Opponent"])):

            if int((dfMajor_Pitching_temp["Year"])[i]) > TeamNames_year:
                TeamNames_yearnumber = TeamNames_year
            else:
                TeamNames_yearnumber = int((dfMajor_Pitching_temp["Year"])[i])

            dfTeamNames_new = dfTeamNames[dfTeamNames["yearID"] == int(TeamNames_yearnumber)].reset_index(drop=True)

            TeamRow = (dfTeamNames_new[dfTeamNames_new["teamIDBR"] == (dfMajor_Fielding_temp["Opponent"])[i]])
            (dfMajor_Fielding_temp["Opponent"])[i] = (list(TeamRow["name"]))[0]

        # Re-order columns to match KNBSB data.
        dfMajor_Fielding_temp = dfMajor_Fielding_temp[["PlayerName", "Team", "Opponent", "HomeGame", "Year", "Month", "Day", "MatchID", "po", "a", "e", "PositionString"]]

        # To add: League, SeasonType
        dfMajor_Fielding_temp.insert(3, "League", "MLB (USA)")
        dfMajor_Fielding_temp.insert(4, "SeasonType", "Post-Season")

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

        for RawPos in dfMajor_Fielding_temp["PositionString"]:
            RawPos = str(RawPos)
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

        dfMajor_Fielding_temp = dfMajor_Fielding_temp.drop(columns=["PositionString"]).reset_index(drop=True)
        dfMajor_Fielding_temp = pd.concat([dfMajor_Fielding_temp, dfPositions], axis=1)

        # Merging the temporary DataFrame with the existing/main DataFrame
        dfMajor_Fielding = pd.concat([dfMajor_Fielding, dfMajor_Fielding_temp]).reset_index(drop=True)


dfMajor_Pitching = dfMajor_Pitching.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)
dfMajor_Batting = dfMajor_Batting.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)
dfMajor_Fielding = dfMajor_Fielding.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)


dfMajor_Pitching.to_csv("Data_retrieval/Results/Major_Pitching.csv", index=False)
dfMajor_Batting.to_csv("Data_retrieval/Results/Major_Batting.csv", index=False)
dfMajor_Fielding.to_csv("Data_retrieval/Results/Major_Fielding.csv", index=False)


import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Major League scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()


