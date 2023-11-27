from numpy.core.arrayprint import _none_or_positive_arg
from numpy.core.numeric import full
import requests
import re
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
from sqlalchemy import create_engine


host = "oege.ie.hva.nl"
username = "minderb002"
password = "+#/tRfRM5zwhnN"
database = "zminderb002"

config = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + "/" + database

engine = create_engine(config)

import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Function to format provided name to correct name
def formatUrl(name, id, league):
    # Replace all the " ' " with a " - "
    if "'" in str(name):
        correctName = name.replace("'", "-")
    else:
        correctName = name
    # Replace all spacebars and " . " with a " - "
    correctName = correctName.replace('.', '-')
    correctName = correctName.replace(' ', '-')
    
    correctName = correctName + "-" + str(id)

    # Replace "--" to "-"
    if "--" in correctName:
        correctName = correctName.replace("--", "-")
    
    # Name to lowercase and league to uppercase
    correctName = correctName.lower()
    league.upper()

    # Check whether it needs a MILB or MLB link 
    if league == "MILB":
        url = "https://www.milb.com/player/" + correctName
    elif league == "MLB":
        url = "https://www.mlb.com/player/" + correctName

    return url


# Function to retrieve data from players in MLB or MILB
# Must provide the correct parameters
def getData(originalName, id, league):
    url = formatUrl(originalName, id, league)
    # Initiating the webdriver. Parameter includes the path of the webdriver.
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
    driver.get(url) 
    
    # This is just to ensure that the page is loaded
    time.sleep(10) 
    driver.implicitly_wait(10)
    
    html = driver.page_source
    # Reading HTML from above URL, using the BeautifulSoup4 library. 
    html = soup(html, "html.parser")

    # Find player container
    playerHeaderBlock = html.find("div", class_="player-header__container")

    # Find all necessary data

    # Not all players have an image
    try:
        image = playerHeaderBlock.find("img", class_="player-headshot")["src"]
    except:
        print("Image not found..")
        image = "N/A"
    
    position = playerHeaderBlock.find("li").text
    height = playerHeaderBlock.find("li", class_="player-header--vitals-height").text.split('/')[0].replace("\' ", "`")

    try:
        age = playerHeaderBlock.find("li", class_="player-header--vitals-age").text.split(": ")[1]
    except:
        print("Age not found..")
        age = "N/A"
    
    summaryBlock = html.find("section", id="summary-block")
    

    # Check if player has a status or something else (MLB site often don't have a status)
    activeStatusIndex = 0
    while True:
        try:
            activeStatus = summaryBlock.findAll("li")[activeStatusIndex].text
            if ("Status:") not in activeStatus:
                activeStatusIndex +=1
            else:
                # activeStatus = activeStatus.split(": ")[1]
                activeStatus = "1"
                break
        except:
            print("Status not found..")
            activeStatus = "?"
            break
    # activeStatus = summaryBlock.findAll("li")[1].text
    # if activeStatus.startswith("Status:"):
    #     activeStatus = summaryBlock.findAll("li")[1].text.split(": ")[1]
    # else:
    #     activeStatus = "N/A"
    
    playerBio = summaryBlock.find("div", class_="player-bio")
    fullname = ""

    # league = "MLB"
    # MILB has other format than MLB
    if league == "MILB":
        fullname = playerBio.find("li", class_="full-name").text
    else:
        fullname = playerBio.find("li", class_="full-name").text.split(": ")[1]


    # Loop through the list elements untill the birthdate is found otherwise use N/A
    # Not all players have a birthday at the same location in the page
    birthDateIndex = 0
    while True:
        try:
            birthDate = playerBio.findAll("li")[birthDateIndex].text
            if "Born:" not in birthDate:
                birthDateIndex +=1
            else :
                birthDate = birthDate.split("\n")[0].split(": ")[1]
                birthDate = birthDate.split("/")[2] + "/" + birthDate.split("/")[0] + "/" + birthDate.split("/")[1]
                birthDate = birthDate.replace("/", "-")
                break
        except:
            print("Birthdate not found..")
            birthDate = "N/A"
            break

    # Find stats container
    statsBlock = summaryBlock.find("div", class_="player-stats-summary-large")

    # Get all hitting (batting) data 
    # Retrieve most recent stat
    try:
        hitting = statsBlock.find("tbody").findAll("tr")[0]
        hitting = statsBlock.findAll("div", class_="responsive-datatable__scrollable")[0]
        playerAB = hitting.find("td", class_="col-1 row-0").find("span").text
        playerR = hitting.find("td", class_="col-2 row-0").find("span").text
        playerH = hitting.find("td", class_="col-3 row-0").find("span").text
        playerHR = hitting.find("td", class_="col-4 row-0").find("span").text
        playerRBI = hitting.find("td", class_="col-5 row-0").find("span").text
        playerSB = hitting.find("td", class_="col-6 row-0").find("span").text
        playerAVG = hitting.find("td", class_="col-7 row-0").find("span").text
        playerOBP = hitting.find("td", class_="col-8 row-0").find("span").text
        playerOPS = hitting.find("td", class_="col-9 row-0").find("span").text
        
        # Creating and adding to csv
        hittingCsv = "wantedHittingPlayer.csv"
        hittingCsvFile = open(hittingCsv, 'w', encoding="utf-8")
        hittingCsvWriter = csv.writer(hittingCsvFile)
        # hittingList = [fullname, id, playerAB, playerR, playerH, playerHR, playerRBI, playerSB, playerAVG, playerOBP, playerOPS]
        hittingList = [fullname, "Null", "Null", "0", "0", playerAB, playerR, playerH, playerRBI, "0", "0", playerHR, "0", playerRBI, "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", playerAVG, playerAVG, playerOBP, playerOBP ,"0" ,"0" ,playerOPS ,playerOPS , "0" , "0"]
        for x in range(1):
            with open(hittingCsv, 'w', newline='') as csvfile:
                hittingCsvWriter.writerow(hittingList)
        hittingCsvFile.close()
    except:
        print("No Batting data available")

    # Get all Pitching data
    # Retrive most recent stat
    try:    
        pitching = statsBlock.findAll("div", class_="responsive-datatable__scrollable")[1]
        pitchingW = pitching.find("td", class_="col-1 row-0").find("span").text
        pitchingL = pitching.find("td", class_="col-2 row-0").find("span").text
        pitchingERA = pitching.find("td", class_="col-3 row-0").find("span").text
        pitchingG = pitching.find("td", class_="col-4 row-0").find("span").text
        pitchingGS = pitching.find("td", class_="col-5 row-0").find("span").text
        pitchingSV = pitching.find("td", class_="col-6 row-0").find("span").text
        pitchingIP = pitching.find("td", class_="col-7 row-0").find("span").text
        pitchingSO = pitching.find("td", class_="col-8 row-0").find("span").text
        pitchingWHIP = pitching.find("td", class_="col-9 row-0").find("span").text

        # Creating and adding to csv
        pitchingCsv = "wantedPitchingPlayers.csv"
        pitchingCsvFile = open(pitchingCsv, 'w', encoding="utf-8")
        pitchingCsvWriter = csv.writer(pitchingCsvFile)
        pitchingList = [fullname, "Null", "Null", pitchingGS, pitchingG, pitchingIP, pitchingIP, "0", "0", "0", "0", pitchingSO, "0", "0", "0", "0", "0", "0", "0", pitchingW, pitchingL, pitchingSV, pitchingERA, pitchingERA, "0", "0", pitchingWHIP, pitchingWHIP, "0", "0", "0", "0", "0", "0", "0", "0"]

        for x in range(1):
            with open(pitchingCsv, 'w', newline='') as csvfile:
                pitchingCsvWriter.writerow(pitchingList)
        pitchingCsvFile.close()
    except: 
        print("No pitching data available")

    #TODO: Check of dit nodig is
    wantedPlayer = "wantedPlayer.csv"

    csvFile = open(wantedPlayer, 'w', encoding="utf-8")
    csvWriter = csv.writer(csvFile)

    playerlist = [id_generator(10), id, image, fullname, birthDate, age, height, "N\A", activeStatus, position]
    
    for x in range(1):
        with open('wantedPlayer.csv', 'w', newline='') as csvfile:
            csvWriter.writerow(playerlist)
    csvFile.close()
    
    wantedPlayerColNames = ["index", "id", "imagelink", "fullname", "birthdate", "currentage", "height", "weight", "active", "position"]
    wantedPlayers = pd.read_csv("wantedPlayer.csv", sep=",", names=wantedPlayerColNames)
    wantedPlayers = wantedPlayers.set_index("index")
    wantedPlayers.to_sql('Player', con=engine, if_exists='append')

    wantedhittingColNames = ["Playername", "FirstAppearance", "LatestAppearance", "g", "pa", "ab", "r", "h", "rbi", "2b", "3b", "hr", "bb", "sb", "cs", "hbp", "sh", "sf", "so", "ibb", "gdp", "po", "a", "e", "MainPos", "Pos_1b", "Pos_2b", "Pos_3b", "Pos_c", "Pos_cf", "Pos_dh", "Pos_lf", "Pos_p", "Pos_ph", "Pos_pr", "Pos_rf", "Pos_ss", "avg_value", "avg_label", "obp_value", "obp_label", "slg_value", "slg_label", "ops_value", "ops_label", "iso_value", "iso_label"]
    wantedHittingPlayers = pd.read_csv("wantedHittingPlayer.csv", sep=",", names=wantedhittingColNames)
    wantedHittingPlayers = wantedHittingPlayers.set_index("Playername")
    wantedHittingPlayers.to_sql("db_Batting_Career", con=engine, if_exists='append')
    
    wantedPitchingColNames = ["Playername", "FirstAppearance", "LatestAppearance", "gs", "g", "ip_value", "ip_label", "h", "r", "er", "bb", "so", "hbp", "ibb", "ab", "bf", "fo", "go", "np", "Win", "Loss", "Save", "era_value", "era_label", "wlp_value", "wlp_label", "whip_value", "whip_label", "h9_value", "h9_label", "bb9_value", "bb9_label", "so9_value", "so9_label", "sobb_value", "sobb_label"]
    wantedPitchingPlayers = pd.read_csv("wantedPitchingPlayers.csv", sep=',', names=wantedPitchingColNames)
    wantedPitchingPlayers = wantedPitchingPlayers.set_index("Playername")
    wantedPitchingPlayers.to_sql("db_Pitching_Career", con=engine, if_exists='append')
    
    # Closing the driver
    driver.close()
