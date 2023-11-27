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
url = [
    "https://www.milb.com/stats",
    "https://www.milb.com/stats/pitching",
    "https://www.milb.com/stats/pacific-coast",
    "https://www.milb.com/stats/pitching/pacific-coast",
    "https://www.milb.com/stats/texas",
    "https://www.milb.com/stats/pitching/texas",
    "https://www.milb.com/stats/eastern",
    "https://www.milb.com/stats/pitching/eastern",
    "https://www.milb.com/stats/southern",
    "https://www.milb.com/stats/pitching/southern",
    "https://www.milb.com/stats/midwest",
    "https://www.milb.com/stats/pitching/midwest",
    "https://www.milb.com/stats/south-atlantic",
    "https://www.milb.com/stats/pitching/south-atlantic",
    "https://www.milb.com/stats/northwest",
    "https://www.milb.com/stats/pitching/northwest",
    "https://www.milb.com/stats/carolina-league",
    "https://www.milb.com/stats/pitching/carolina-league",
    "https://www.milb.com/stats/florida-state",
    "https://www.milb.com/stats/pitching/florida-state",
    "https://www.milb.com/stats/california",
    "https://www.milb.com/stats/pitching/california",
]

ChromeDriverManager().install

chrome_options = Options()
chrome_options.add_argument("--headless")
all_players_name_id = {}

for i in range(len(url)):
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url[i]) 
        
    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html = driver.page_source
    # Reading HTML from above URL, using the BeautifulSoup4 library. 

    html = soup(html, "html.parser")
    navigationNumber = html.findAll("button", class_="button-3wq5VxsJ tab-27nhZTIl sm-1_yhMOW5 default-theme-3rNrN4ik")
    for j in range(len(navigationNumber)):
        url.append(url[i] + "/?page=" + str(j + 2))
driver.close()

for i in range(len(url)):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
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