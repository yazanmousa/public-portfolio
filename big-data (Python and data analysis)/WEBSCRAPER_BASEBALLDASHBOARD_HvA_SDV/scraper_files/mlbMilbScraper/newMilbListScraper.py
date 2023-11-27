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

# urls
url = ["https://www.milb.com/stats/hitting",
"https://www.milb.com/stats/pitching"
]
ChromeDriverManager().install
all_players_name_id = {}
for i in range(len(url)):
    # Options so selenium does not open the browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url[i]) 
        
    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html = driver.page_source
    # Reading HTML from above URL, using the BeautifulSoup4 library. 

    html = soup(html, "html.parser")

    # Find all buttons where class is equal to the class of the navigation numbers
    navigationNumber = html.findAll("button", class_="button-3wq5VxsJ tab-27nhZTIl sm-1_yhMOW5 default-theme-3rNrN4ik")

    # Loop through the navigation numbers and add the url to the url list
    for j in range(len(navigationNumber)):
        # Check which page it is on, hitting or pitching
        if (i == 0):
            url.append("https://www.milb.com/stats/?page=" + str(j + 2))
        elif (i == 1):
            url.append("https://www.milb.com/stats/pitching/?page=" + str(j + 2))

# Loop through the urls and scrape all players and their ids
for i in range(len(url)):
    driver.get(url[i])
    time.sleep(5) 

    html = driver.page_source
    html = soup(html, "html.parser")

    # Find all A elements with class
    allAElement = html.findAll("a", class_="bui-link")

    # Delete two unnecessary links
    del allAElement[1]
    del allAElement[0]

    # Find all the playersname and id and put into dictionary
    for i in range(len(allAElement)):
        playersName = allAElement[i]["aria-label"]
        playersId = allAElement[i]["href"].split("/")[2]
        all_players_name_id[playersName] = playersId

driver.close()

# Convert dictionary to dataframe
df = pd.DataFrame.from_dict(all_players_name_id, orient="index").reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill="")

# Rename columns
df = df.rename(columns={"index": "Name", 0 : "Id"})

# Add column league and assign MILB to all data
df["league"] = "MILB"

# Overwrite csv file 
df.to_csv("newAllMilbPlayers.csv", index=False)

import datetime
filename = '../Data_retrieval/Scripts/Log.txt'
text = open(filename, 'r').read()
text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    new milb list scraping completed.\n' + text

text_file = open(filename, 'w')
text_file.write(text)
text_file.close()

