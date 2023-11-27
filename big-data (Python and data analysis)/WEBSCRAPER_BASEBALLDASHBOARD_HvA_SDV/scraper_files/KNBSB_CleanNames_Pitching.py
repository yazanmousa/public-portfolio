

import requests, re
from urllib.parse import urljoin
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import json


AllPlayers = pd.DataFrame()

SeasonURLs = [
    'https://www.baseball-reference.com/register/league.cgi?id=cd410b9b',
    'https://www.baseball-reference.com/register/league.cgi?id=d747b98b',
    'https://www.baseball-reference.com/register/league.cgi?id=fa2a0371',
    'https://www.baseball-reference.com/register/league.cgi?id=268c5d1e',
    'https://www.baseball-reference.com/register/league.cgi?id=373945df',
    'https://www.baseball-reference.com/register/league.cgi?id=9c37d8b7',
    'https://www.baseball-reference.com/register/league.cgi?id=398f7908',
    'https://www.baseball-reference.com/register/league.cgi?id=107e48d7',
    'https://www.baseball-reference.com/register/league.cgi?id=82c46f37',
    'https://www.baseball-reference.com/register/league.cgi?id=07c5f45a',
    'https://www.baseball-reference.com/register/league.cgi?id=60811a5b'
]


for url in SeasonURLs:
    req = Request(url, headers={"User-Agent":"Mozilla/5.0"})

    page_html = urlopen(req).read()
    page_soup = str(soup(page_html, "html.parser"))

    table = page_soup[page_soup.find('id="league_batting"'):]
    table = table[:table.find("</table>")]
    
    rows = table.split('<tr')[2:-1]

    for row in rows:
        href = row[row.find('<a href="/register/team.cgi?id=')+9:]
        href = 'https://www.baseball-reference.com' + href[:href.find('"')]
        
        req = Request(href, headers={"User-Agent":"Mozilla/5.0"})

        page_html = urlopen(req).read()
        page_soup = soup(page_html, "html.parser")
        page_soup_str = str(page_soup)

        RosterTable = page_soup_str[page_soup_str.find('id="div_standard_roster"'):]
        RosterTable = RosterTable[RosterTable.find("<table"):RosterTable.find("</table>")+8]

        teamname = str(page_soup.findAll("h1",{"itemprop":"name"})).split("\n")[2]
        teamname = teamname[teamname.find('>')+1:teamname.rfind('<')]
        season = str(page_soup.findAll("h1",{"itemprop":"name"})).split("\n")[1]
        season = season[season.find('>')+1:season.rfind('<')]
        roster = pd.read_html(RosterTable)[0][['Name']]
        roster.insert(1, 'Team', teamname)
        roster.insert(2, 'Year', season)
        AllPlayers = pd.concat([AllPlayers, roster]).reset_index(drop=True)


# Load all teams with all teamname-variations (file is maintained manually).
with open("Data_retrieval/Scripts/Necessities/KNBSB_AllTeams.txt") as f:
    AllTeams = json.load(f)


# Match and modify all teamnames to the correct, most current teamname.
AllPlayers.insert(2, 'Team_Year', '')
AllPlayers.insert(1, 'KNBSB_Name', '')

for i in range(len(AllPlayers['Team'])):
    for team in AllTeams:
        if AllPlayers['Team'][i] in team:
            AllPlayers['Team'][i] = team[0]
    
    AllPlayers['Team_Year'][i] = str(AllPlayers['Team'][i]) + '_' + str(AllPlayers['Year'][i])



dfPitching = pd.read_csv("Data_retrieval/Results/KNBSB_Pitching.csv")
dfPitching.insert(1, 'Team_Year', '')
for i in range(len(dfPitching['Team'])):
    for team in AllTeams:
        if dfPitching['Team'][i] in team:
            dfPitching['Team'][i] = team[0]
        if dfPitching['Opponent'][i] in team:
            dfPitching['Opponent'][i] = team[0]

    dfPitching['Team_Year'][i] = str(dfPitching['Team'][i]) + '_' + str(dfPitching['Year'][i])

dfPitching.insert(1, 'New_Name', '')


All_Team_Year = AllPlayers.groupby(['Team', 'Year'], as_index=False).count()[['Team', 'Year']].sort_values(['Year', 'Team'], ascending=(True, True)).reset_index(drop=True)
All_Team_Year.insert(0, 'Team_Year', '')
for i in range(len(All_Team_Year['Team_Year'])):
    All_Team_Year['Team_Year'][i] = str(All_Team_Year['Team'][i]) + '_' + str(All_Team_Year['Year'][i])


dfPitching_NoRoster = pd.DataFrame()
for i in range(len(dfPitching['PlayerName'])):
    if dfPitching['Team_Year'][i] not in list(All_Team_Year['Team_Year']):
        dfPitching_NoRoster = pd.concat([dfPitching_NoRoster, dfPitching.iloc[i:i+1,:]])

dfPitching_NoRoster = dfPitching_NoRoster.reset_index(drop=True)


dfPitching_WithRoster = pd.DataFrame()
for i in range(len(dfPitching['PlayerName'])):
    if dfPitching['Team_Year'][i] in list(All_Team_Year['Team_Year']):
        dfPitching_WithRoster = pd.concat([dfPitching_WithRoster, dfPitching.iloc[i:i+1,:]])

dfPitching_WithRoster = dfPitching_WithRoster.reset_index(drop=True)



dfPitching_AutoMatch = pd.DataFrame()

for Team_Year in All_Team_Year['Team_Year']:
    Pitching_temp = dfPitching_WithRoster[dfPitching_WithRoster['Team_Year'] == Team_Year].reset_index(drop=True)
    AllPlayers_temp = AllPlayers[AllPlayers['Team_Year'] == Team_Year].reset_index(drop=True)

    for i in range(len(Pitching_temp['PlayerName'])):
        Name = Pitching_temp['PlayerName'][i].split(' ')[0].capitalize()
        NameMatches = pd.DataFrame()
        for x in range(len(AllPlayers_temp['Name'])):
            if Name in AllPlayers_temp['Name'][x]:
                NameMatches = pd.concat([NameMatches, AllPlayers_temp.iloc[x:x+1,:]])

        if NameMatches.empty == True:
            pass
        elif len(NameMatches['Name']) == 1:
            Pitching_temp['New_Name'][i] = list(NameMatches['Name'])[0]
            for z in range(len(AllPlayers_temp['KNBSB_Name'])):
                if Pitching_temp['New_Name'][i] == AllPlayers_temp['Name'][z]:
                    AllPlayers_temp['KNBSB_Name'][z] = Pitching_temp['PlayerName'][i]
        else:
            if Pitching_temp['PlayerName'][i].count(' ') > 0:
                Initials = Pitching_temp['PlayerName'][i].split(' ')[-1]
                for Name in NameMatches['Name']:
                    FirstName = Name.split(' ')[0]
                    if Initials.lower() == FirstName[:len(Initials)].lower():
                        Pitching_temp['New_Name'][i] = Name
                        for z in range(len(AllPlayers_temp['KNBSB_Name'])):
                            if Pitching_temp['New_Name'][i] == AllPlayers_temp['Name'][z]:
                                AllPlayers_temp['KNBSB_Name'][z] = Pitching_temp['PlayerName'][i]

    NoMatch = Pitching_temp[Pitching_temp['New_Name'] == ''].reset_index(drop=True)
    AllPlayers_NoMatch = AllPlayers_temp[AllPlayers_temp['KNBSB_Name'] == ''].reset_index(drop=True)
    Pitching_AutoMatched = Pitching_temp[Pitching_temp['New_Name'] != ''].reset_index(drop=True)

    for i in range(len(NoMatch['PlayerName'])):
        Name = NoMatch['PlayerName'][i].split(' ')[0].capitalize()
        NameMatches = pd.DataFrame()
        for x in range(len(AllPlayers_NoMatch['Name'])):
            if Name in AllPlayers_NoMatch['Name'][x]:
                NameMatches = pd.concat([NameMatches, AllPlayers_NoMatch.iloc[x:x+1,:]])

        if NameMatches.empty == True:
            pass
        elif len(NameMatches['Name']) == 1:
            NoMatch['New_Name'][i] = list(NameMatches['Name'])[0]
            for z in range(len(AllPlayers_NoMatch['KNBSB_Name'])):
                if NoMatch['New_Name'][i] == AllPlayers_NoMatch['Name'][z]:
                    AllPlayers_NoMatch['KNBSB_Name'][z] = NoMatch['PlayerName'][i]
        else:
            if NoMatch['PlayerName'][i].count(' ') > 0:
                Initials = NoMatch['PlayerName'][i].split(' ')[-1]
                for Name in NameMatches['Name']:
                    FirstName = Name.split(' ')[0]
                    if Initials.lower() == FirstName[:len(Initials)].lower():
                        NoMatch['New_Name'][i] = Name
                        for z in range(len(AllPlayers_NoMatch['KNBSB_Name'])):
                            if NoMatch['New_Name'][i] == AllPlayers_NoMatch['Name'][z]:
                                AllPlayers_NoMatch['KNBSB_Name'][z] = NoMatch['PlayerName'][i]

    dfPitching_AutoMatch = pd.concat([dfPitching_AutoMatch, Pitching_AutoMatched, NoMatch]).reset_index(drop=True)



dfPitching_NoAutoMatch = dfPitching_AutoMatch[dfPitching_AutoMatch['New_Name'] == ''].reset_index(drop=True)
AllPlayers_Manual = pd.read_csv('Data_retrieval/Scripts/Necessities/KNBSB_AllPlayers_Manual.csv').dropna().reset_index(drop=True)

dfPitching_ManualMatch = pd.concat([dfPitching_NoAutoMatch, dfPitching_NoRoster]).reset_index(drop=True)
dfPitching_ManualMatch.insert(2, 'status', '')

for i in range(len(dfPitching_ManualMatch['PlayerName'])):
    for x in range(len(AllPlayers_Manual['KNBSB_Name'])):
        if dfPitching_ManualMatch['PlayerName'][i] == AllPlayers_Manual['KNBSB_Name'][x]:
            dfPitching_ManualMatch['New_Name'][i] = AllPlayers_Manual['FullName'][x]
            dfPitching_ManualMatch['status'][i] = 'matched (manually)'


dfPitching_AutoMatch = dfPitching_AutoMatch[dfPitching_AutoMatch['New_Name'] != ''].reset_index(drop=True)
dfPitching_AutoMatch.insert(2, 'status', 'matched')


dfPitching_new = pd.concat([dfPitching_ManualMatch, dfPitching_AutoMatch]).reset_index(drop=True)

for i in range(len(dfPitching_new['PlayerName'])):
    if dfPitching_new['New_Name'][i] != '':
        dfPitching_new['PlayerName'][i] = dfPitching_new['New_Name'][i]


dfPitching_new = dfPitching_new.drop(['New_Name', 'status', 'Team_Year'], axis=1)

dfPitching_new = dfPitching_new.sort_values(['PlayerName', 'Year', 'Month', 'Day', 'MatchID'], ascending=(True, False, False, False, True)).reset_index(drop=True)

dfPitching_new.to_csv("Data_retrieval/Results/KNBSB_Pitching.csv", index=False)


import datetime
filename = 'Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    KNBSB pitcher names cleaned.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

