#main script of the project big data
#imports
import pandas as pd
import scraper_2021


def batting_stats_2021():
    #dataframe batting
    #get the dictionary from the scraper
    batting = scraper_2021.batting_stats()

    #from this dict, make a dataframe
    batting_df = pd.DataFrame.from_dict(batting)
    #the player name have new lines printed in them, so replace those with " "
    batting_df['player'] = batting_df['player'].str.replace("\n", " ")

    return batting_df


def pitching_stats_2021():
    #dataframe pitching
    #get the dictionary from the scraper
    pitching = scraper_2021.pitching_stats()

    #from this dict, make a dataframe
    pitching_df = pd.DataFrame.from_dict(pitching)
    #the player name have new lines printed in them, so replace those with " "
    pitching_df['player'] = pitching_df['player'].str.replace("\n", " ")

    return pitching_df


def fielding_stats_2021():
    #dataframe batting
    #get the dictionary from the scraper
    fielding = scraper_2021.fielding_stats()

    #from this dict, make a dataframe
    fielding_df = pd.DataFrame.from_dict(fielding)
    #the player name have new lines printed in them, so replace those with " "
    fielding_df['player'] = fielding_df['player'].str.replace("\n", " ")

    return fielding_df

batting = batting_stats_2021()
pitching = pitching_stats_2021()
fielding = fielding_stats_2021()

batting.to_csv("2021_batting.csv", index=False)
pitching.to_csv("2021_pitching.csv", index=False)
fielding.to_csv("2021_fielding.csv", index=False)