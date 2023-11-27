from _typeshed import OpenBinaryModeUpdating
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

# urls
url = "https://www.mlb.com/players"

all_players_name_id = {}

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
playersDiv = html.find("div", id="players-index")
playersAElement = playersDiv.findAll("a", class_="p-related-links__link")
for i in range(len(playersAElement)):
    playersName = playersAElement[i].text
    playersId = playersAElement[i]["href"].split("-")
    playersId = playersId[len(playersId) - 1]

    all_players_name_id[playersName] = playersId

driver.close()

# Convert dictionary to dataframe
df = pd.DataFrame.from_dict(all_players_name_id, orient="index").reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill="")

# Rename columns
df = df.rename(columns={"index": "Name", 0 : "Id"})

# Add column league and assign MLB to all data
df["league"] = "MLB"

# Overwrite csv file
df.to_csv("allMlbPlayers.csv", index=False)

import datetime
filename = '../Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    mlb list scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()
