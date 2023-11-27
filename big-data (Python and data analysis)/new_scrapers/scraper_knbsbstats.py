#creator: Marco Jansen, 500826312, Hogeschool van Amsterdam

#imports
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

import time

#create scraper driver
driver = webdriver.Chrome("chromedriver.exe")

#go to scrape page
driver.get("https://www.knbsbstats.nl/")

#wait for page to load
WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located)


#scraping regular competition
def scraper_19_20():    
    #find all "Reguliere competitie" links
    regular_comp = driver.find_elements_by_link_text("Reguliere competitie")
    #this will also give the regular competition series of softbal so we will delete the odd indexes
    #to skip over the softbal links
    del regular_comp[1::2]

    #click the regular_comp links
    for link in regular_comp:
        link.click()

    #find all tabs
    reg_comp_tabs = driver.window_handles

    #make empty lists to store the field data, which is then stored within row data
    row_data = []
    field_data = []

    #loop through open tabs, skipping the first tap
    for window in reg_comp_tabs[1:]:
        #select the tab which is looped over
        driver.switch_to_window(window)
        #find the link for the statistics and click it
        driver.find_element_by_partial_link_text("Individual Statistics").click()
        #wait for everything to load in
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located)
        #find the second tbody tag. In this tag are all the rows needed located
        body_elem = driver.find_elements_by_css_selector("tbody")
        body_elem = body_elem[1]
        #get all rows of value. So not the label rows in blue
        rows = body_elem.find_elements_by_css_selector("tr")
        #get fields for every row
        for row in rows:
            fields = row.find_elements_by_css_selector("td")
            #get the data from every field in the rows
            for field in fields:
                #add it into a list
                field_data.append(field.text)
            #add the year which is found in the second h1 element and add it per row
            field_data.append(driver.find_elements_by_xpath("//h1")[1].text[-4:])
            #add the list with field data to the list to fill it with row information
            row_data.append(field_data)
            #empty the list for the upcomming rows
            field_data = []
        driver.close()
        driver.switch_to_window(reg_comp_tabs[0])
        
    #creating labels for the dataframe
    labels = ['Player',
            'avg',
            'gp-gs',
            'ab',
            'r',
            'h',
            '2b',
            '3b',
            'hr',
            'rbi',
            'tb',
            'slg%',
            'bb',
            'hbp',
            'so',
            'gdp',
            'ob%',
            'sf',
            'sh',
            'sb-att',
            'year']

    #make a dataframe to store the lists
    df = pd.DataFrame(row_data, columns=labels)

    return df


def scraper_10_18():    
    #go back to the home page
    driver.get("https://www.knbsbstats.nl/")
    #wacht 5 seconden, want de pagina refreashed eerst nog eens
    time.sleep(5)

    #find all "Hoofdklasse" links
    hoofdklasse = driver.find_elements_by_link_text("Hoofdklasse")
    #certain years have "hoofdklasse" in both honkbal and softball, but we need only honkbal
    #there is no consistent patern so we need to make a list of indexes on our own
    honkbal_indexes = [0,1,2,3,4,6,8,10,12]
    #the new hoofdklasse list will later on be used to click the links
    hoofdklasse = [hoofdklasse[i] for i in honkbal_indexes]

    #click the regular_comp links
    for link in hoofdklasse:
        link.click()

    #find all tabs
    hoofdklasse_tabs = driver.window_handles

    #make empty lists to store the field data, which is then stored within row data
    row_data = []
    field_data = []

    #loop through open tabs, skipping the first tap
    for window in hoofdklasse_tabs[1:]:
        #select the tab which is looped over
        driver.switch_to_window(window)
        #find the link for the statistics and click it
        driver.find_element_by_partial_link_text("Individual Statistics").click()
        #wait for everything to load in
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located)
        #find the second tbody tag. In this tag are all the rows needed located
        body_elem = driver.find_elements_by_css_selector("tbody")
        body_elem = body_elem[1]
        #get all rows of value. So not the label rows in blue
        rows = body_elem.find_elements_by_css_selector("tr")
        #get fields for every row
        for row in rows:
            fields = row.find_elements_by_css_selector("td")
            #get the data from every field in the rows
            for field in fields:
                #add it into a list
                field_data.append(field.text)
            #add the year which is found in the second h1 element and add it per row
            field_data.append(driver.find_elements_by_xpath("//h1[text()[contains(., 'Hoofdklasse')]]")[0].text[-4:])
            #add the list with field data to the list to fill it with row information
            row_data.append(field_data)
            #empty the list for the upcomming rows
            field_data = []
        driver.close()
        
    #creating labels for the dataframe
    labels = ['Player',
            'avg',
            'gp-gs',
            'ab',
            'r',
            'h',
            '2b',
            '3b',
            'hr',
            'rbi',
            'tb',
            'slg%',
            'bb',
            'hbp',
            'so',
            'gdp',
            'ob%',
            'sf',
            'sh',
            'sb-att',
            'year']

    #make a dataframe to store the lists
    df = pd.DataFrame(row_data, columns=labels)
    return df

#run the scrapers and put the f
df_19_20 = scraper_19_20()
df_10_18 = scraper_10_18()

#clean the data
df_10_18_clean = df_10_18.drop(df_10_18.index[df_10_18["Player"] == "Player "])
df_19_20_clean = df_19_20.drop(df_19_20.index[df_19_20["Player"] == "Player "])
#There are also some rows with "----------", These also need to be removed
df_10_18_clean = df_10_18_clean.drop(df_10_18_clean.index[df_10_18_clean["Player"] == "----------"])
df_19_20_clean = df_19_20_clean.drop(df_19_20_clean.index[df_19_20_clean["Player"] == "----------"])

#There was also 1 page per scraper which did not get the correct year, but instead got kbal as value
#this also need to be changed by replacing it with the right year
df_10_18_clean["year"] = df_10_18_clean["year"].str.replace("kbal", "2016")
df_19_20_clean["year"] = df_19_20_clean["year"].str.replace("KBAL", "2020")

#lastly we put the data in csv files
df_10_18_clean.to_csv("stats_10-18.csv", index=False)
df_19_20_clean.to_csv("stats_19-20.csv", index=False)