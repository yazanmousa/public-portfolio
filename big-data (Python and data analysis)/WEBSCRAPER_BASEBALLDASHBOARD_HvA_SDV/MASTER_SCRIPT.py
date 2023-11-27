import schedule
import time
import datetime
# from MySQL_data import load_SQL_table
from sqlalchemy import create_engine
import os

def dataCollection():
    filename = 'log/Log.txt'
    text = open(filename, 'r').read()
    text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Master script automatically initiated.\n' + text

    text_file = open(filename, 'w')
    text_file.write(text)
    text_file.close()

    # import TournamentEurope_Africa
    # import TournamentWorldCup
    # import TournamentXXIX_WorldCup
    # import TournamentXXVII_WorldCup
    # import TournamentPremier12Scraper
    # import scraper_files.mlbMilbScraper.newMilbListScraper
    # import scraper_files.mlbMilbScraper.mlbListScraper
    # import scraper_files.mergeAllPlayersToSQL
    import scraper_files.KNBSB
    import scraper_files.KNBSB_CleanNames_BatFld
    import scraper_files.KNBSB_CleanNames_Pitching
    import scraper_files.Honkbalsite
    import scraper_files.MajorLeague
    import scraper_files.MinorLeague
    import scraper_files.CombiningCSVsToSQL
    import scraper_files.GamelogsToYearly
    import scraper_files.CalculateStats_Batting
    import scraper_files.CalculateStats_Fielding
    import scraper_files.CalculateStats_Pitching 
    

    SQL_Engine = create_engine(os.getenv('SQL_Credentials'))
    SQL_Time = datetime.datetime.utcnow().strftime('%B %d, %Y - %H:%M UTC')
    SQL_Engine.connect().execute("UPDATE app_settings SET value = '" + SQL_Time + "' WHERE item = 'last_data_update'")

    filename = 'log/Log.txt'
    text = open(filename, 'r').read()
    text = '[' + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ']    Master script completed.\n' + text
    
    text_file = open(filename, 'w')
    text_file.write(text)
    text_file.close()

dataCollection()
# Run every night at 3 AM docker uses UTC time
# schedule.every().day.at("01:00").do(dataCollection)
# while True:
#     schedule.run_pending()
#     now = datetime.datetime.now()
#     nextRun = schedule.next_run()
#     print('Current Time: ', now.strftime("%H:%M:%S"), 'Next Run at: ', nextRun.strftime("%H:%M:%S"))
#     time.sleep(60)