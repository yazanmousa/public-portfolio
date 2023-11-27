
import requests, re
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup


# This module is used for reading CSV files and replacing certain parts.
import pandas as pd
import numpy as np

# This module is used for converting strings to a date and/or time.
from datetime import datetime

# Define the header titles.
Headers_Batting = ["PlayerName", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hp", "sh", "sf", "so", "ibb", "kl", "gdp", "po", "a", "e"]
Headers_Pitching_new = ["PlayerName", "ip", "h", "r", "er", "bb", "so", "wp", "bk", "hbp", "ibb", "ab", "bf", "fo", "go", "np"]
Headers_Pitching_2010_2011 = ["PlayerName", "ip", "h", "r", "er", "bb", "so", "wp", "bk", "hbp", "ibb", "ab", "bf", "fo", "go"]

# Create the main (empty) dataframes.
dfBatting_Main = pd.DataFrame()
dfPitching_Main = pd.DataFrame()

# Define a formula that converts a list to a single-column DataFrame
def List_to_DF(List):
    df = pd.DataFrame([List]).transpose()
    return df

# Define a formula that scrapes all URLs from a given page.
def get_links(url):
    from bs4 import BeautifulSoup as soup
    import requests, re
    from urllib.parse import urljoin

    r = requests.get(url)
    main_soup = soup(r.text, "html.parser")
    a_tags = main_soup.find_all("a", href=re.compile(r''))
    links = [urljoin(url, a["href"])for a in a_tags]
    return links

def page_exists(url):
    from bs4 import BeautifulSoup as soup
    import requests, re

    r = requests.get(url)
    main_soup = soup(r.text, "html.parser")
    title = main_soup.find("title").text
    if 'Pagina niet gevonden' in title:
        return False
    else:
        return True


StatPages = get_links('https://www.knbsbstats.nl/archief/')
StatPages = [x for x in StatPages if "/HB/statsHB" in x]
StatPages = [x for x in StatPages if page_exists(x) == True]
StatPages.sort()


for page in StatPages:
    base_url = page[:page.rfind('/')+1]
    Year = page[page.find('.nl/')+4:page.find('.nl/')+8]

    category = page[:page.rfind('/')]
    category = category[category.rfind('/')+1:]

    if category == 'statsHB':
        SeasonType = 'Regular Season'
    else:
        SeasonType = 'Post-Season'

    MatchIDs = get_links(page)
    MatchIDs = [x[x.rfind('/')+1:x.rfind('.')] for x in MatchIDs]

    MatchIDs = [x for x in MatchIDs if x[-3:].isdigit() == True]

    for Raw_MatchID in MatchIDs:
        url = base_url + Raw_MatchID + '.htm'
        req = Request(url, headers={"User-Agent":"Mozilla/5.0"})

        if '-' in Raw_MatchID:
            MatchID = Raw_MatchID[Raw_MatchID.find('-')+1:]
        else:
            MatchID = Raw_MatchID

        page_html = urlopen(req).read()
        page_soup = soup(page_html, "html.parser")

        AllTables = page_soup.findAll("table",{"cellpadding":"2"})

        MatchHeader = page_soup.find("h3").text
        DayMonthStr = MatchHeader[MatchHeader.find("(")+1:MatchHeader.find(")")-4]
        DayMonthStr = DayMonthStr.replace(",", "").strip()

        if Year == "2015":
            if MatchID == "356":
                DayMonthStr = "May 14"

        if "June" in DayMonthStr:
            DayMonthStr = DayMonthStr.replace("June", "Jun")

        if "July" in DayMonthStr:
            DayMonthStr = DayMonthStr.replace("July", "Jul")

        DayMonthObj = datetime.strptime(DayMonthStr, "%b %d")
        MatchMonth = DayMonthObj.strftime("%m")
        MatchDay = DayMonthObj.strftime("%d")
        
        HomeTeamName = MatchHeader[MatchHeader.find(" vs ")+4:MatchHeader.find("(")-1]
        AwayTeamName = MatchHeader[0:MatchHeader.find(" vs ")]

        # This section matches the correct table to the name. 
        AwayTeam_batting = str(AllTables[0])
        HomeTeam_batting = str(AllTables[1])
        Pitching = str(AllTables[2])

        # Read HTML strings (tables) into Pandas Dataframe.
        dfBatting_temp1 = pd.read_html(AwayTeam_batting, header=0)[0]
        dfBatting_temp2 = pd.read_html(HomeTeam_batting, header=0)[0]
        dfPitching_tempAll = pd.read_html(Pitching, header=0)[0]

        # Split Pitching Temp file into two separate files.
        dfPitching_tempAll = dfPitching_tempAll.iloc[::2].reset_index(drop=True)
        dfPitching_list = np.split(dfPitching_tempAll, dfPitching_tempAll[dfPitching_tempAll.isnull().all(1)].index)
        dfPitching_temp1 = dfPitching_list[0]
        dfPitching_temp1.dropna(inplace=True)
        dfPitching_temp1 = dfPitching_temp1.reset_index(drop=True)
        dfPitching_temp2 = dfPitching_list[1]
        dfPitching_temp2.dropna(inplace=True)
        dfPitching_temp2 = dfPitching_temp2.reset_index(drop=True)

        # Remove the "Totals" row from the Dataframes (not applicable to pitching tables).
        dfBatting_temp1 = dfBatting_temp1[:-1]
        dfBatting_temp2 = dfBatting_temp2[:-1]

        # Replace Team Name in header with "PlayerName" (header list is above).
        dfBatting_temp1.columns = Headers_Batting
        dfBatting_temp2.columns = Headers_Batting

        if Year == "2010" or Year == "2011":
            dfPitching_temp1.columns = Headers_Pitching_2010_2011
            dfPitching_temp2.columns = Headers_Pitching_2010_2011
            dfPitching_temp1.insert(15, "np", 0)
            dfPitching_temp2.insert(15, "np", 0)
        else:
            dfPitching_temp1.columns = Headers_Pitching_new
            dfPitching_temp2.columns = Headers_Pitching_new

        # Adding new columns with Team name, Opponent, League, Home or Away game (hot-encoding), Position, ...
        Batting_NamePos1 = (dfBatting_temp1["PlayerName"].str.rsplit(" ", n=1)).to_list()
        dfBatting_NamePos1 = pd.DataFrame(Batting_NamePos1, columns=["PlayerName", "PositionString"])
        Batting_NamePos2 = (dfBatting_temp2["PlayerName"].str.rsplit(" ", n=1)).to_list()
        dfBatting_NamePos2 = pd.DataFrame(Batting_NamePos2, columns=["PlayerName", "PositionString"])

        dfBatting_temp1 = dfBatting_temp1.drop(columns=["PlayerName"])
        dfBatting_temp2 = dfBatting_temp2.drop(columns=["PlayerName"])

        dfBatting_temp1 = pd.concat([dfBatting_NamePos1, dfBatting_temp1], axis=1)
        dfBatting_temp2 = pd.concat([dfBatting_NamePos2, dfBatting_temp2], axis=1)

        dfBatting_temp1.insert(2, "Team", AwayTeamName)
        dfBatting_temp1.insert(3, "Opponent", HomeTeamName)
        dfBatting_temp1.insert(4, "League", "Hoofdklasse Honkbal (NLD)")
        dfBatting_temp1.insert(5, "SeasonType", SeasonType)
        dfBatting_temp1.insert(6, "HomeGame", 0)
        dfBatting_temp1.insert(7, "Year", Year)
        dfBatting_temp1.insert(8, "Month", MatchMonth)
        dfBatting_temp1.insert(9, "Day", MatchDay)
        dfBatting_temp1.insert(10, "MatchID", MatchID)

        dfBatting_temp2.insert(2, "Team", HomeTeamName)
        dfBatting_temp2.insert(3, "Opponent", AwayTeamName)
        dfBatting_temp2.insert(4, "League", "Hoofdklasse Honkbal (NLD)")
        dfBatting_temp2.insert(5, "SeasonType", SeasonType)
        dfBatting_temp2.insert(6, "HomeGame", 1)
        dfBatting_temp2.insert(7, "Year", Year)
        dfBatting_temp2.insert(8, "Month", MatchMonth)
        dfBatting_temp2.insert(9, "Day", MatchDay)
        dfBatting_temp2.insert(10, "MatchID", MatchID)


        dfPitching_temp1.insert(1, "Team", AwayTeamName)
        dfPitching_temp1.insert(2, "Opponent", HomeTeamName)
        dfPitching_temp1.insert(3, "League", "Hoofdklasse Honkbal (NLD)")
        dfPitching_temp1.insert(4, "SeasonType", SeasonType)
        dfPitching_temp1.insert(5, "HomeGame", 0)
        dfPitching_temp1.insert(6, "Year", Year)
        dfPitching_temp1.insert(7, "Month", MatchMonth)
        dfPitching_temp1.insert(8, "Day", MatchDay)
        dfPitching_temp1.insert(9, "MatchID", MatchID)

        dfPitching_temp2.insert(1, "Team", HomeTeamName)
        dfPitching_temp2.insert(2, "Opponent", AwayTeamName)
        dfPitching_temp2.insert(3, "League", "Hoofdklasse Honkbal (NLD)")
        dfPitching_temp2.insert(4, "SeasonType", SeasonType)
        dfPitching_temp2.insert(5, "HomeGame", 1)
        dfPitching_temp2.insert(6, "Year", Year)
        dfPitching_temp2.insert(7, "Month", MatchMonth)
        dfPitching_temp2.insert(8, "Day", MatchDay)
        dfPitching_temp2.insert(9, "MatchID", MatchID)

        # Adding the game-started column to the pitching DF.
        for df in [dfPitching_temp1, dfPitching_temp2]:
            df.insert(10, "gs", 0)
            for i in range(len(df["gs"])):
                if i == 0: # Only first player in temp table is the game starter.
                    df["gs"][i] = 1
                else:
                    df["gs"][i] = 0

        # Adding new column to batting files with positions played (hot-encoding)
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

        for RawPos1 in dfBatting_temp1["PositionString"]:

            if "/" in RawPos1:
                FirstPos = RawPos1[:RawPos1.find("/")]
                SecondPos = RawPos1[RawPos1.find("/")+1:]
            else:
                FirstPos = RawPos1
                SecondPos = ""

            if FirstPos == "1b" or SecondPos == "1b":
                df1b.append(1)
            else:
                df1b.append(0)

            if FirstPos == "2b" or SecondPos == "2b":
                df2b.append(1)
            else:
                df2b.append(0)

            if FirstPos == "3b" or SecondPos == "3b":
                df3b.append(1)
            else:
                df3b.append(0)

            if FirstPos == "c" or SecondPos == "c":
                dfc.append(1)
            else:
                dfc.append(0)

            if FirstPos == "cf" or SecondPos == "cf":
                dfcf.append(1)
            else:
                dfcf.append(0)

            if FirstPos == "dh" or SecondPos == "dh":
                dfdh.append(1)
            else:
                dfdh.append(0)

            if FirstPos == "lf" or SecondPos == "lf":
                dflf.append(1)
            else:
                dflf.append(0)

            if FirstPos == "p" or SecondPos == "p":
                dfp.append(1)
            else:
                dfp.append(0)

            if FirstPos == "ph" or SecondPos == "ph":
                dfph.append(1)
            else:
                dfph.append(0)

            if FirstPos == "pr" or SecondPos == "pr":
                dfpr.append(1)
            else:
                dfpr.append(0)

            if FirstPos == "rf" or SecondPos == "rf":
                dfrf.append(1)
            else:
                dfrf.append(0)

            if FirstPos == "ss" or SecondPos == "ss":
                dfss.append(1)
            else:
                dfss.append(0)

        df1b = List_to_DF(df1b)
        df2b = List_to_DF(df2b)
        df3b = List_to_DF(df3b)
        dfc = List_to_DF(dfc)
        dfcf = List_to_DF(dfcf)
        dfdh = List_to_DF(dfdh)
        dflf = List_to_DF(dflf)
        dfp = List_to_DF(dfp)
        dfph = List_to_DF(dfph)
        dfpr = List_to_DF(dfpr)
        dfrf = List_to_DF(dfrf)
        dfss = List_to_DF(dfss)
        
        dfPositions1 = pd.concat([df1b, df2b, df3b, dfc, dfcf, dfdh, dflf, dfp, dfph, dfpr, dfrf, dfss], axis=1)
        dfPositions1.columns = ["Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss", ]

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

        for RawPos2 in dfBatting_temp2["PositionString"]:

            if "/" in RawPos2:
                FirstPos = RawPos2[:RawPos2.find("/")]
                SecondPos = RawPos2[RawPos2.find("/")+1:]
            else:
                FirstPos = RawPos2
                SecondPos = ""

            if FirstPos == "1b" or SecondPos == "1b":
                df1b.append(1)
            else:
                df1b.append(0)

            if FirstPos == "2b" or SecondPos == "2b":
                df2b.append(1)
            else:
                df2b.append(0)

            if FirstPos == "3b" or SecondPos == "3b":
                df3b.append(1)
            else:
                df3b.append(0)

            if FirstPos == "c" or SecondPos == "c":
                dfc.append(1)
            else:
                dfc.append(0)

            if FirstPos == "cf" or SecondPos == "cf":
                dfcf.append(1)
            else:
                dfcf.append(0)

            if FirstPos == "dh" or SecondPos == "dh":
                dfdh.append(1)
            else:
                dfdh.append(0)

            if FirstPos == "lf" or SecondPos == "lf":
                dflf.append(1)
            else:
                dflf.append(0)

            if FirstPos == "p" or SecondPos == "p":
                dfp.append(1)
            else:
                dfp.append(0)

            if FirstPos == "ph" or SecondPos == "ph":
                dfph.append(1)
            else:
                dfph.append(0)

            if FirstPos == "pr" or SecondPos == "pr":
                dfpr.append(1)
            else:
                dfpr.append(0)

            if FirstPos == "rf" or SecondPos == "rf":
                dfrf.append(1)
            else:
                dfrf.append(0)

            if FirstPos == "ss" or SecondPos == "ss":
                dfss.append(1)
            else:
                dfss.append(0)

        df1b = List_to_DF(df1b)
        df2b = List_to_DF(df2b)
        df3b = List_to_DF(df3b)
        dfc = List_to_DF(dfc)
        dfcf = List_to_DF(dfcf)
        dfdh = List_to_DF(dfdh)
        dflf = List_to_DF(dflf)
        dfp = List_to_DF(dfp)
        dfph = List_to_DF(dfph)
        dfpr = List_to_DF(dfpr)
        dfrf = List_to_DF(dfrf)
        dfss = List_to_DF(dfss)

        dfPositions2 = pd.concat([df1b, df2b, df3b, dfc, dfcf, dfdh, dflf, dfp, dfph, dfpr, dfrf, dfss], axis=1)
        dfPositions2.columns = ["Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss", ]

        dfBatting_temp1 = dfBatting_temp1.drop(columns=["PositionString"])
        dfBatting_temp1 = pd.concat([dfBatting_temp1, dfPositions1], axis=1)

        dfBatting_temp2 = dfBatting_temp2.drop(columns=["PositionString"])
        dfBatting_temp2 = pd.concat([dfBatting_temp2, dfPositions2], axis=1)


        # Adding new column to Pitching files with Win/Lose/Save (hot-encoding)
        Win = []
        Loss = []
        Save = []
        PitcherName_new = []

        dfPitching_temp1_headers = list(dfPitching_temp1.columns.values)

        for PitcherName in dfPitching_temp1["PlayerName"]:
            if "," in PitcherName:
                OldName = PitcherName[:PitcherName.find(",")-1]
                OldName = OldName.strip()
            else:
                OldName = PitcherName
                OldName = OldName.strip()

            LastTwo = OldName[-2:]
            if LastTwo == " W":
                Win.append(1)
                NewName = OldName.replace(" W", "").strip()
                NewName = NewName.strip()
                PitcherName_new.append(NewName)
            else:
                Win.append(0)
            
            if LastTwo == " L":
                Loss.append(1)
                NewName = OldName.replace(" L", "")
                NewName = NewName.strip()
                PitcherName_new.append(NewName)
            else:
                Loss.append(0)
            
            if LastTwo == " S":
                Save.append(1)
                NewName = OldName.replace(" S", "")
                NewName = NewName.strip()
                PitcherName_new.append(NewName)
            else:
                Save.append(0)
            
            if LastTwo != " W" and LastTwo != " L" and LastTwo != " S":
                PitcherName_new.append(OldName)

        PitcherName_new = List_to_DF(PitcherName_new)

        Win = List_to_DF(Win)
        Loss = List_to_DF(Loss)
        Save = List_to_DF(Save)

        dfPitching_temp1 = dfPitching_temp1.drop(columns=["PlayerName"])

        dfPitching_temp1 = pd.concat([PitcherName_new, dfPitching_temp1, Win, Loss, Save], axis=1)

        dfPitching_temp1_headers.append("Win")
        dfPitching_temp1_headers.append("Loss")
        dfPitching_temp1_headers.append("Save")

        dfPitching_temp1.columns = dfPitching_temp1_headers

        # Reset variables for dfPitching_temp2
        Win = []
        Loss = []
        Save = []
        PitcherName_new = []

        dfPitching_temp2_headers = list(dfPitching_temp2.columns.values)

        for PitcherName in dfPitching_temp2["PlayerName"]:
            if "," in PitcherName:
                OldName = PitcherName[:PitcherName.find(",")-1]
            else:
                OldName = PitcherName

            LastTwo = OldName[-2:]
            if LastTwo == " W":
                Win.append(1)
                NewName = OldName.replace(" W", "")
                PitcherName_new.append(NewName)
            else:
                Win.append(0)
            
            if LastTwo == " L":
                Loss.append(1)
                NewName = OldName.replace(" L", "")
                PitcherName_new.append(NewName)
            else:
                Loss.append(0)
            
            if LastTwo == " S":
                Save.append(1)
                NewName = OldName.replace(" S", "")
                PitcherName_new.append(NewName)
            else:
                Save.append(0)
            
            if LastTwo != " W" and LastTwo != " L" and LastTwo != " S":
                PitcherName_new.append(OldName)

        PitcherName_new = List_to_DF(PitcherName_new)

        Win = List_to_DF(Win)
        Loss = List_to_DF(Loss)
        Save = List_to_DF(Save)

        dfPitching_temp2 = dfPitching_temp2.drop(columns=["PlayerName"])

        dfPitching_temp2 = pd.concat([PitcherName_new, dfPitching_temp2, Win, Loss, Save], axis=1)

        dfPitching_temp2_headers.append("Win")
        dfPitching_temp2_headers.append("Loss")
        dfPitching_temp2_headers.append("Save")

        dfPitching_temp2.columns = dfPitching_temp2_headers

        # Concatenate Temp Dataframes into main Dataframe.
        dfBatting_Main = pd.concat([dfBatting_Main, dfBatting_temp1, dfBatting_temp2]).reset_index(drop=True)
        dfPitching_Main = pd.concat([dfPitching_Main, dfPitching_temp1, dfPitching_temp2]).reset_index(drop=True)


dfBatting_Main.columns = ["PlayerName", "Team", "Opponent", "League", "SeasonType", "HomeGame", "Year", "Month", "Day", "MatchID", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "kl", "gdp", "po", "a", "e", "Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss"]
dfPitching_Main.columns = ["PlayerName", "Team", "Opponent", "League", "SeasonType", "HomeGame", "Year", "Month", "Day", "MatchID", "gs", "ip", "h", "r", "er", "bb", "so", "wp", "bk", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save"]

dfPitching_Main[['np']] = dfPitching_Main[['np']].fillna(0)



dfBatting_Main = dfBatting_Main.drop(["kl"], axis=1).reset_index(drop=True)
dfPitching_Main = dfPitching_Main.drop(["wp", "bk"], axis=1).reset_index(drop=True)


dfBatting_Main = dfBatting_Main.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)
dfPitching_Main = dfPitching_Main.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)


dfBatting_Main.to_csv("Results/KNBSB_Batting.csv", index=False)
dfPitching_Main.to_csv("Results/KNBSB_Pitching.csv", index=False)


import datetime
filename = 'log/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    KNBSB scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

