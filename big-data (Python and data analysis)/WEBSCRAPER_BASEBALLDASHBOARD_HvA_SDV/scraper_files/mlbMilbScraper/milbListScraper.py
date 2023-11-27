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

# host = "oege.ie.hva.nl"
# username = "minderb002"
# password = "+#/tRfRM5zwhnN"
# database = "zminderb002"

# config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

# SQL_Engine = create_engine(config)
###################################

# Main url to scrape from
mainUrl = "https://www.milb.com/stats/"

# List of urls we scrape player data from
urlList = []

# Dictionary to store players and their id
all_players_name_id = {}

# Options so selenium does not open the browser
chrome_options = Options()
chrome_options.add_argument("--headless")

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
driver.get(mainUrl) 

# this is just to ensure that the page is loaded
time.sleep(5) 

html = driver.page_source
# Reading HTML from above URL, using the BeautifulSoup4 library. 
html = soup(html, "html.parser")

# get all links
allAElement = html.findAll("a", class_="p-button__link p-button--regular")

# Check if batting or pitching substring is in the corresponding link, if so add to list
# to get the most recent data
for i in range(len(allAElement)):
    battingString = "http://www.milb.com/milb/stats/stats.jsp?sid=milb&t=l_bat&lid"
    pitchingString = "http://www.milb.com/milb/stats/stats.jsp?sid=milb&t=l_pit&lid"
    link = html.findAll("a", class_="p-button__link p-button--regular")[i]["href"]
    if battingString in link or pitchingString in link:
        urlList.append(link)


# Loop through all urls and scrape data
for url in urlList:
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
    driver.get(url) 

    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html = driver.page_source
    # Reading HTML from above URL, using the BeautifulSoup4 library. 
    html = soup(html, "html.parser")

    # Searching the HTML element with its content for div with ID = stats_data
    stats_data = html.find("div", id="stats_data")
    
    # Find all the <td> with the class dg-player_id within the stats_data div
    playerid = stats_data.findAll("td", class_="dg-player_id")

    # Find all the <td> with the class dg-name_display_first_last within the stats_data div
    playernamediv = stats_data.findAll("td", class_="dg-name_display_first_last")

    # Dictionary of name paired with id
    for (id, name) in zip(playerid, playernamediv):
        all_players_name_id[name.text] = id.text


# Closing the driver
driver.close()

# Convert dictionary to dataframe
df = pd.DataFrame.from_dict(all_players_name_id, orient="index").reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill="")

# Rename columns
df = df.rename(columns={"index": "Name", 0 : "Id"})

# Add column league and assign MILB to all data
df["league"] = "MILB"

# Overwrite csv file 
df.to_csv("allMilbPlayers.csv", index=False)

import datetime
filename = '../Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    asdasdsadasdsa list scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()