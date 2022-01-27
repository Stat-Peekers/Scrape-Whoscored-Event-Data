# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:28:34 2020
@title: Scrape event level data for all matches not in current data in local directory
@author: Sushant Rao
@twitter: @footyfan08 / @StatPeekers
"""

import os
import main
import pandas as pd
from selenium import webdriver
from shutil import copy2


if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')

    # getting competition urls
    league_urls = main.getLeagueUrls()

    # Select comp and season:
    tournaments_list = ["Premier League"]
    season_list = ["2021-2022"]
    # Get input for tournament details:
    for i, text_output in enumerate(tournaments_list, start=1):
        print("{}. {}".format(i, text_output))
    while True:
        try:
            selected = int(input('Select one of the below (1-{}): '.format(i)))
            comp_name = tournaments_list[selected - 1]
            print('Selected Tournament is {}'.format(comp_name))
            break
        except(ValueError, IndexError):
            print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

    for i, text_output in enumerate(season_list, start=1):
        print("{}. {}".format(i, text_output))
    while True:
        try:
            selected = int(input('Select one of the below (1-{}): '.format(i)))
            season_name = season_list[selected - 1]
            print('Selected Season is {}'.format(season_name))
            break
        except(ValueError, IndexError):
            print('This is not a valid selection. Please enter number between 1 and {}!'.format(i))

    # getting match urls for that competition and season
    match_urls = main.getMatchUrls(comp_urls=league_urls, competition=comp_name, season=season_name)

    # getting match data for the matches not already scraped (eg. since 3rd match of PL)
    data_dir = "../data/" + str(comp_name) + "/" + str(season_name.replace("/", "-")) + "/"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Read already existing file:
    df = pd.read_csv(data_dir + "event_data.csv")
    n_matches = df["matchId"].nunique()

    # matches_data = main.getMatchesData(match_urls=team_urls[:5])
    matches_data = main.getMatchesData(match_urls=match_urls[n_matches:])

    # getting events dataframe for required matches
    events_ls = [main.createEventsDF(match) for match in matches_data]

    # adding EPV column
    events_list = [main.addEpvToDataFrame(match) for match in events_ls]
    events_dfs = pd.concat(events_list)

    # Append new data to old data:
    df = df.append(events_dfs)

    # saving events as csv
    copy2(data_dir + 'event_data.csv', data_dir + 'event_data_copy.csv')
    df.to_csv(data_dir + 'event_data.csv', index=False)
