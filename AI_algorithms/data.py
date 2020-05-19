import sys
import os
import pickle
import pandas as pd

from constants import TEAMS, STATS_TYPE, HEADERS, ADDITIONAL_STATS_TYPE
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.library.parameters import SeasonTypeAllStar
from process import create_mean_std_dev_dicts, z_score_difference
from utils import get_team_stats

home_path = os.getcwd()

# Get the normalized Z-scores of the games played based on the home and away team stats, mean, and std dev
def get_z_scores_list(game, mean_dict, std_dev_dict, startDate, endDate, season):
    home_team = list(game.items())[0]
    away_team = list(game.items())[0]
    games = [home_team["label"], away_team["label"]]
    
    home_stats = get_team_stats(home_team["name"], home_team["start_date"], home_team["end_date"], home_team["season"], use_cached_stats)
    away_stats = get_team_stats(away_team["name"], away_team["start_date"], away_team["end_date"], away_team["season"], use_cached_stats)
    
    for stat, statType in ADDITIONAL_STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
        z_score_dif = z_score_difference(home_stats[stat], away_stats[stat], mean_dict[stat], std_dev_dict[stat])
        games.append(z_score_dif)
        
    return [games]

# Get the data and the Zscore differentials of each game
def get_data(game, season, start_of_season, current_date):
    data_dicts = create_mean_std_dev_dicts(start_of_season, current_date, season)
    if not data_dicts or not data_dicts[0] or not data_dicts[1]: # If we got no data
        empty = pd.DataFrame()
        return empty
    mean_dict = data_dicts[0]
    std_dev_dict = data_dicts[1]

    # Call get Zscore helper function
    games = get_z_scores_list(game, mean_dict, std_dev_dict, start_of_season, current_date, season)
    # Use Pandas dataframe to hold
    game_with_z_score_difs = pd.DataFrame(
		games,
		columns=[
            'Home','Away','W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
        'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
        'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE',
        ]
	)

    return game_with_z_score_difs

def main():
    # Whichever year we want the data for.
    if len(sys.argv) < 2:
        print("Wrong usage")
        sys.exit()
    else:
        season_year = int(sys.argv[1])
    # season_year = 2011
    gamefinder = leaguegamelog.LeagueGameLog(season=season_year, season_type_all_star=SeasonTypeAllStar.default)
    games = gamefinder.get_data_frames()[0]
    previous_team = games['TEAM_NAME'][0]
    start_of_season = games['GAME_DATE'][0]
    end_of_season = games['GAME_DATE'][games.shape[0] - 1]
    if start_of_season[2] == '0' and start_of_season[3] != '9':
        season = start_of_season[:4] + '-0' + str(int(start_of_season[2:4])+1)
    else:
        season = start_of_season[:4] + '-' + str(int(start_of_season[2:4])+1)

    # download_helper_DF = pd.read_csv(home_path+'/Data/gamesWithInfo' + season + '.csv')
    # # If for some reason your program stopped running, continue progress by 
    # # settiing this to the last index that was downloaded.
    # # !!! When -1, it will reset whatever file you were saving to so be careful !!!
    # If download helper exists, get it and retrieve last index
    last_index_downloaded = -10
    for file in os.listdir(home_path+'/Data/'):
        if 'DownloadHelper' + season + '.csv' in file:
            df = pd.read_csv(home_path + '/Data/DownloadHelper' + season + '.csv')
            last_index_downloaded = int(df['lastIndex'])
            
    # For a given season, iterate through all the games
    for index, row in games.iterrows():
        if last_index_downloaded == -10:
            print("NEED TO SET LAST INDEX")
            sys.exit()
        if index <= last_index_downloaded:
            continue
        if index % 2 != 0:
            current_team = row['TEAM_NAME']
            game = {previous_team: current_team}
            game_date = row['GAME_DATE']

            game_stat = get_data(game, season, start_of_season, game_date)
            if game_stat.empty: # If we got no data
                continue
            winLoss = row['WL']
            if winLoss == 'W':
                game_stat['Result'] = 0
            else:
                game_stat['Result'] = 1

            year = game_date[:4]
            month = game_date[5:7]
            day = game_date[-2:]
            new_date_format = month + '/' + day + '/' + year
            game_stat['Date'] = new_date_format

            percent_done = (index + 1) / games.shape[0] # Total number of games
            percent_done *= 100
            print('['+str(index)+'] Progress: ' + str(round(percent_done, 2)) + '%', " | ", 'Season ' + season, previous_team + ' vs ' + current_team)

            if index == 1:
                # Initialize the file with headers. This function resets the file.
                game_stat.to_csv(home_path + '/Data/gamesWithMorInfo' + season + '.csv')
            else:
                # Keep track of last downloaded index and season year
                download_helper_data = {'lastIndex' : [index]}
                download_helper_DF = pd.DataFrame(download_helper_data, columns = ['lastIndex'])
                download_helper_DF.to_csv(home_path + '/TestTrainingData/DownloadHelper' + season + '.csv')
                with open(home_path+'/TestTrainingData/gamesWithMoreInfo'+season+'.csv','a') as file:
                    game_stat.to_csv(file, header=False)
        else:
            previous_team = row['TEAM_NAME']

if __name__ == "__main__":
	main()