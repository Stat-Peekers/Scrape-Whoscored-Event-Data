# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:28:34 2020

@author: Sushant Rao
@twitter: @footyfan08 / @StatPeekers
"""

import os
import sys
import main
import pandas as pd
from selenium import webdriver


"""
Get data for multiple matches

New: Now added xG data for shots from Understat.com(only available for top 5 european leagues since 2014-15).
"""

# ==     Get Match Data  (Run from line 29 to line 35 together)      == #
if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')

    # ==    Get data for multiple matches    == #
    # getting competition urls
    league_urls = main.getLeagueUrls()

    # getting match urls for that competition and season
    match_urls = main.getMatchUrls(comp_urls=league_urls, competition='Premier League', season='2021/2022')

    # getting match urls for a specific team
    team_name = 'Liverpool'
    team_urls = main.getTeamUrls(team=team_name, match_urls=match_urls)

    # getting match data for the required urls(eg. first 5 matches of Barcelona)
    # matches_data = main.getMatchesData(match_urls=team_urls[:5])
    matches_data = main.getMatchesData(match_urls=team_urls)

    # getting events dataframe for required matches
    events_ls = [main.createEventsDF(match) for match in matches_data]

    # adding EPV column
    events_list = [main.addEpvToDataFrame(match) for match in events_ls]
    events_dfs = pd.concat(events_list)

    # saving events as csv

    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    sys.path.append(src_dir)
    os.chdir(src_dir)
    data_dir = "data/" + str(team_name) + "/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    events_dfs.to_csv(data_dir + 'event_data.csv', index=False)
