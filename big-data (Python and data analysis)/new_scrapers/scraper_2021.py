#Marco Jansen, 500826312, Hogeschool van Amsterdam

#selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

driver = webdriver.Chrome('chromedriver.exe')

def batting_stats():
    #go to the batting link
    driver.get("https://stats.knbsbstats.nl/en/events/2021-hoofdklasse-honkbal/stats/general/874/batting")

    #wait for the page elements to be loaded
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'stats-content')))
    
    #make an empty dict to store the values
    batting_dict = {"player": [],
                    "team": [],
                    "AB": [],
                    "R": [],
                    "H": [],
                    "2B": [],
                    "3B": [],
                    "HR": [],
                    "RBI": [],
                    "TB": [],
                    "AVG": [],
                    "SLG": [],
                    "OBP": [],
                    "OPS": [],
                    "BB": [],
                    "HBP": [],
                    "SO": [],
                    "GDP": [],
                    "SF": [],
                    "SH": [],
                    "SB": [],
                    "CS": []}

    #find the element with all rows inside of it
    element = driver.find_element_by_class_name('table-condensed')
    #find rows with player data within this element
    rows = element.find_elements_by_css_selector('tr[data-index]')
    #go through these rows and per append all field values into the previously created dictionary
    for row in rows:
        batting_dict["player"].append(row.find_element_by_class_name("player").text)
        batting_dict["team"].append(row.find_element_by_class_name("team").text)
        batting_dict["AB"].append(row.find_element_by_class_name("ab").text)
        batting_dict["R"].append(row.find_element_by_class_name("r").text)
        batting_dict["H"].append(row.find_element_by_class_name("h").text)
        batting_dict["2B"].append(row.find_element_by_class_name("double").text)
        batting_dict["3B"].append(row.find_element_by_class_name("triple").text)
        batting_dict["HR"].append(row.find_element_by_class_name("hr").text)
        batting_dict["RBI"].append(row.find_element_by_class_name("rbi").text)
        batting_dict["TB"].append(row.find_element_by_class_name("tb").text)
        batting_dict["AVG"].append(row.find_element_by_class_name("avg").text)
        batting_dict["SLG"].append(row.find_element_by_class_name("slg").text)
        batting_dict["OBP"].append(row.find_element_by_class_name("obp").text)
        batting_dict["OPS"].append(row.find_element_by_class_name("ops").text)
        batting_dict["BB"].append(row.find_element_by_class_name("bb").text)
        batting_dict["HBP"].append(row.find_element_by_class_name("hbp").text)
        batting_dict["SO"].append(row.find_element_by_class_name("so").text)
        batting_dict["GDP"].append(row.find_element_by_class_name("gdp").text)
        batting_dict["SF"].append(row.find_element_by_class_name("sf").text)
        batting_dict["SH"].append(row.find_element_by_class_name("sh").text)
        batting_dict["SB"].append(row.find_element_by_class_name("sb").text)
        batting_dict["CS"].append(row.find_element_by_class_name("cs").text)

    return batting_dict

def pitching_stats():
    #go to the batting link
    driver.get("https://stats.knbsbstats.nl/en/events/2021-hoofdklasse-honkbal/stats/general/874/pitching")

    #wait for the page elements to be loaded
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'stats-content')))
    
    #make an empty dict to store the values
    pitching_dict = {"player": [],
                    "team": [],
                    "W": [],
                    "L": [],
                    "ERA": [],
                    "APP": [],
                    "GS": [],
                    "SV": [],
                    "CG": [],
                    "SHO": [],
                    "IP": [],
                    "H": [],
                    "R": [],
                    "ER": [],
                    "BB": [],
                    "SO": [],
                    "2B": [],
                    "3B": [],
                    "HR": [],
                    "AB": [],
                    "BAVG": [],
                    "WP": [],
                    "HBP": [],
                    "BK": [],
                    "SFA": [],
                    "SHA": [],
                    "GO": [],
                    "FO": []}

    #find the element with all rows inside of it
    element = driver.find_element_by_class_name('table-condensed')
    #find rows with player data within this element
    rows = element.find_elements_by_css_selector('tr[data-index]')
    #go through these rows and per append all field values into the previously created dictionary
    for row in rows:
        pitching_dict["player"].append(row.find_element_by_class_name("player").text)
        pitching_dict["team"].append(row.find_element_by_class_name("team").text)
        pitching_dict["W"].append(row.find_element_by_class_name("pitch_win").text)
        pitching_dict["L"].append(row.find_element_by_class_name("pitch_loss").text)
        pitching_dict["ERA"].append(row.find_element_by_class_name("era").text)
        pitching_dict["APP"].append(row.find_element_by_class_name("pitch_appear").text)
        pitching_dict["GS"].append(row.find_element_by_class_name("pitch_gs").text)
        pitching_dict["SV"].append(row.find_element_by_class_name("pitch_save").text)
        pitching_dict["CG"].append(row.find_element_by_class_name("pitch_cg").text)
        pitching_dict["SHO"].append(row.find_element_by_class_name("pitch_sho").text)
        pitching_dict["IP"].append(row.find_element_by_class_name("pitch_ip").text)
        pitching_dict["H"].append(row.find_element_by_class_name("pitch_h").text)
        pitching_dict["R"].append(row.find_element_by_class_name("pitch_r").text)
        pitching_dict["ER"].append(row.find_element_by_class_name("pitch_er").text)
        pitching_dict["BB"].append(row.find_element_by_class_name("pitch_bb").text)
        pitching_dict["SO"].append(row.find_element_by_class_name("pitch_so").text)
        pitching_dict["2B"].append(row.find_element_by_class_name("pitch_double").text)
        pitching_dict["3B"].append(row.find_element_by_class_name("pitch_triple").text)
        pitching_dict["HR"].append(row.find_element_by_class_name("pitch_hr").text)
        pitching_dict["AB"].append(row.find_element_by_class_name("pitch_ab").text)
        pitching_dict["BAVG"].append(row.find_element_by_class_name("bavg").text)
        pitching_dict["WP"].append(row.find_element_by_class_name("pitch_wp").text)
        pitching_dict["HBP"].append(row.find_element_by_class_name("pitch_hbp").text)
        pitching_dict["BK"].append(row.find_element_by_class_name("pitch_bk").text)
        pitching_dict["SFA"].append(row.find_element_by_class_name("pitch_sfa").text)
        pitching_dict["SHA"].append(row.find_element_by_class_name("pitch_sha").text)
        pitching_dict["GO"].append(row.find_element_by_class_name("pitch_ground").text)
        pitching_dict["FO"].append(row.find_element_by_class_name("pitch_fly").text)

    return pitching_dict

def fielding_stats():
    #go to the batting link
    driver.get("https://stats.knbsbstats.nl/en/events/2021-hoofdklasse-honkbal/stats/general/874/fielding")

    #wait for the page elements to be loaded
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'stats-content')))
    
    #make an empty dict to store the values
    fielding_dict = {"player": [],
                    "team": [],
                    "G": [],
                    "C": [],
                    "PO": [],
                    "A": [],
                    "E": [],
                    "FLDP": [],
                    "DP": [],
                    "SBA": [],
                    "CSB": [],
                    "SBAP": [],
                    "PB": [],
                    "CI": []}

    #find the element with all rows inside of it
    element = driver.find_element_by_class_name('table-condensed')
    #find rows with player data within this element
    rows = element.find_elements_by_css_selector('tr[data-index]')
    #go through these rows and append all field values into the previously created dictionary
    for row in rows:
        fielding_dict["player"].append(row.find_element_by_class_name("player").text)
        fielding_dict["team"].append(row.find_element_by_class_name("team").text)
        fielding_dict["G"].append(row.find_element_by_class_name("field_g").text)
        fielding_dict["C"].append(row.find_element_by_class_name("field_c").text)
        fielding_dict["PO"].append(row.find_element_by_class_name("field_po").text)
        fielding_dict["A"].append(row.find_element_by_class_name("field_a").text)
        fielding_dict["E"].append(row.find_element_by_class_name("field_e").text)
        fielding_dict["FLDP"].append(row.find_element_by_class_name("fldp").text)
        fielding_dict["DP"].append(row.find_element_by_class_name("field_dp").text)
        fielding_dict["SBA"].append(row.find_element_by_class_name("field_sba").text)
        fielding_dict["CSB"].append(row.find_element_by_class_name("field_csb").text)
        fielding_dict["SBAP"].append(row.find_element_by_class_name("sbap").text)
        fielding_dict["PB"].append(row.find_element_by_class_name("field_pb").text)
        fielding_dict["CI"].append(row.find_element_by_class_name("field_ci").text)

    return fielding_dict

# batting = batting_stats()
# pitching = pitching_stats()
# fielding = fielding_stats()

# df_batting = pd.DataFrame(batting)
# df_batting['player'] = df_batting['player'].str.replace("\n", " ")
# df_batting.to_csv("2021_batting.csv", index=False)

# df_pitching = pd.DataFrame(pitching)
# df_pitching['player'] = df_pitching['player'].str.replace("\n", " ")
# df_pitching.to_csv("2021_pitching.csv", index=False)

# df_fielding = pd.DataFrame(fielding)
# df_fielding['player'] = df_fielding['player'].str.replace("\n", " ")
# df_fielding.to_csv("2021_fielding.csv", index=False)