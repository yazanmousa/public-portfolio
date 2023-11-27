import requests
import re
from sqlalchemy import create_engine
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
import csv
###################################

host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

SQL_Engine = create_engine(config)
###################################

# urls
url = "https://u18bwc.wbsc.org/en/2017/stats/general/team/NED"

allTournamentStatsScraper = []

# Options so selenium does not open the browser
chrome_options = Options()
chrome_options.add_argument("--headless")

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
driver.get(url) 
    
# this is just to ensure that the page is loaded
time.sleep(5) 

html = driver.page_source
# Reading HTML from above URL, using the BeautifulSoup4 library. 
html = soup(html, "html.parser")

# Searching the HTML element with its content for div with ID = stats_data
playersDiv = html.find("div", class_="fixed-table-body")
playersAElement = playersDiv.findAll("td", class_="goto-link player")
abAElement = playersDiv.findAll("td", class_="goto-link ab")
rAElement = playersDiv.findAll("td", class_="goto-link r")
hAElement = playersDiv.findAll("td", class_="goto-link h")
doubleAElement = playersDiv.findAll("td", class_="goto-link double")
tripleAElement = playersDiv.findAll("td", class_="goto-link triple")
hrAElement = playersDiv.findAll("td", class_="goto-link hr")
rbiAElement = playersDiv.findAll("td", class_="goto-link rbi")
tbAElement = playersDiv.findAll("td", class_="goto-link tb")
avgAElement = playersDiv.findAll("td", class_="goto-link avg")
slgAElement = playersDiv.findAll("td", class_="goto-link slg")
obpAElement = playersDiv.findAll("td", class_="goto-link obp")
opsAElement = playersDiv.findAll("td", class_="goto-link ops")
bbAElement = playersDiv.findAll("td", class_="goto-link bb")
hbpAElement = playersDiv.findAll("td", class_="goto-link hbp")
soAElement = playersDiv.findAll("td", class_="goto-link so")
gdpAElement = playersDiv.findAll("td", class_="goto-link gdp")
sfAElement = playersDiv.findAll("td", class_="goto-link sf")
shAElement = playersDiv.findAll("td", class_="goto-link sh")
sbAElement = playersDiv.findAll("td", class_="goto-link sb")
csAElement = playersDiv.findAll("td", class_="goto-link cs")

for i in range(len(playersAElement)):
    abStat = abAElement[i].text
    rStat = rAElement[i].text
    hStat = hAElement[i].text
    doubleStat = doubleAElement[i].text
    tripleStat= tripleAElement[i].text
    hrStat = hrAElement[i].text
    rbiStat = rbiAElement[i].text
    tbStat = tbAElement[i].text
    avgStat = avgAElement[i].text
    slgStat = slgAElement[i].text
    obpStat = obpAElement[i].text
    opsStat = opsAElement[i].text
    bbStat = bbAElement[i].text
    hbpStat = hbpAElement[i].text
    soStat = soAElement[i].text
    gdpStat = gdpAElement[i].text
    sfStat = sfAElement[i].text
    shStat = shAElement[i].text
    sbStat = sbAElement[i].text
    csStat = csAElement[i].text
    playersName = playersAElement[i].text
    playersId = playersAElement[i]["data-link"].split("/")
    playersId = playersId[len(playersId) - 1]

    data = [playersName, playersId, abStat, rStat, hStat, doubleStat, tripleStat, hrStat, rbiStat, tbStat, avgStat, slgStat, 
    obpStat, opsStat, bbStat, hbpStat, soStat, gdpStat, sfStat, shStat, sbStat, csStat]


    allTournamentStatsScraper.append(data)
    allTournamentStats = pd.DataFrame(allTournamentStatsScraper, columns=["Name","id","ab","r","h","2B","3B","hr","rbi","tb","avg","slg","obp",
    "ops","bb","hbp","so","gdp","sf","sh","sb","cs"])
    
driver.close()

# Convert dictionary to dataframe
# df = pd.DataFrame.from_dict(all_players_name_id, orient="index").reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill="")

# Rename columns
# df = df.rename(columns={"index": "Name", 0 : "Id"})
allTournamentStats['Year'] = '2017'
allTournamentStats['Tournament'] = 'U-18-WorldCup'
allTournamentStats = allTournamentStats[['Name','Tournament','Year','id','ab','r','h','2B','3B','hr','rbi','tb','avg','slg','obp','ops','bb','hbp','so','gdp','sf','sh','sb','cs']]
# Overwrite csv file
allTournamentStats.to_csv("U-18-WorldCup-2017.csv", index=False)