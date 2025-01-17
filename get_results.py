#import drivers
from bs4 import BeautifulSoup as bs
import pandas as pd
import geckodriver_autoinstaller
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
geckodriver_autoinstaller.install()

#Set Chrome options
options = webdriver.ChromeOptions()
options.headless = True  # Change to True for headless mode (no browser window)
options.page_load_strategy = 'normal'
#load web browser
driver = webdriver.Chrome(options=options)
#create array
matches = []
results = []
#for each year in the six nations get the webpage and get the scores
for i in tqdm(range(2000,2025)):
    #open webpage based on year
    url = "https://www.sixnationsrugby.com/en/m6n/fixtures/{0}?tab=matches".format(i) #change year 
    #get webpage
    driver.get(url)
    #give it time to load
    time.sleep(5)
    #parse webpage
    soup = bs(driver.page_source, "html.parser")


    #get scores
    year = i
    # loop each round
    for round_no in tqdm(range(1, 6)):
        #get round info
        round_div = soup.find("div", {"id": "roundNumber-{0}".format(round_no)})
        round_info = round_div.get_text(separator=',', strip=True)
        #split round info into matches
        matches = round_info.split('Match centre')
        for match in matches:
            if len(match) > 2:
                match_details = match.split(',')
                # Remove empty strings
                match_details = [x for x in match_details if x.strip()]
                #check to see if a Sunday game and adjust accordingly
                if len(match_details) > 9:
                    round_date = match_details[0]
                    stadium = match_details[1]
                    homeTeam = match_details[2]
                    awayTeam = match_details[8]
                    finalscoreHome = match_details[3]
                    finalscoreAway = match_details[9]
                    HTscoreHome = match_details[5]
                    HTScoreAway = match_details[7]
                else: 
                    stadium = match_details[0]
                    homeTeam = match_details[1]
                    awayTeam = match_details[7]
                    finalscoreHome = match_details[2]
                    finalscoreAway = match_details[8]
                    HTscoreHome = match_details[4]
                    HTScoreAway = match_details[6]
                # info from matches
              
                
                #add to results
                results.append([year, round_no, round_date, stadium, homeTeam, awayTeam, finalscoreHome,  finalscoreAway, HTscoreHome, HTScoreAway])
        

#close webdriver
driver.quit()
#creat dataframe
final_table = pd.DataFrame(results, columns = ['Year', 'Round', 'Date', 'Stadium', 'HomeTeam', 'AwayTeam', 'FinalScoreHome', 'FinalScoreAway', 'HTScoreHome', 'HTScoreAway'])
#save to csv
final_table.to_csv('data/SixNationsResults.csv', index=False)
print (final_table)