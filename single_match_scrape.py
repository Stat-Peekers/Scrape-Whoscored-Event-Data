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

    # whoscored match centre url of the required match (Example: Barcelona vs Sevilla)
    url = "https://1xbet.whoscored.com/Matches/1549632/Live/England-Premier-League-2021-2022-Liverpool-Brighton"
    match_data = main.getMatchData(driver, url, close_window=True)

    # Match dataframe containing info about the match
    matches_df = main.createMatchesDF(match_data)

    # Events dataframe
    events_df = main.createEventsDF(match_data)

    # match Id
    matchId = match_data['matchId']

    # Information about respective teams as dictionary
    home_data = matches_df['home'][matchId]
    away_data = matches_df['away'][matchId]

    # ==     Get EPV for successful passes     == #
    events_df = main.addEpvToDataFrame(events_df)

    # saving events as csv

    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    sys.path.append(src_dir)
    os.chdir(src_dir)
    tour_name = match_data["league"]
    ht_name = match_data["home"]["name"]
    at_name = match_data["away"]["name"]
    season = match_data["season"].replace("/", "-")
    data_dir = "data/" + str(tour_name) + "/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    events_df.to_csv(data_dir + 'event_data_' + ht_name + '_vs_' + at_name + '_' + season + '.csv', index=False)

