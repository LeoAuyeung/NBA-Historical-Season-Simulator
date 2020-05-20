import sys
import os
import pickle
import pandas as pd

from constants import TEAMS, STATS_TYPE, HEADERS, ADDITIONAL_STATS_TYPE
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.library.parameters import SeasonTypeAllStar
from process import create_mean_std_dev_dicts, z_score_difference
from utils import get_team_stats_2

home_path = os.getcwd()

# Get the normalized Z-scores of the games played based on the home and away team stats, mean, and std dev
def get_z_scores_list(game, mean_dict, std_dev_dict, startDate, endDate, season):
    homeTeam, awayTeam = list(game.items())[0]
    gameAsList = [homeTeam, awayTeam]
    homeTeamStats = get_team_stats_2(homeTeam, startDate, endDate, season)
    awayTeamStats = get_team_stats_2(awayTeam, startDate, endDate, season)
    
    for stat, statType in ADDITIONAL_STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
        zScoreDif = z_score_difference(homeTeamStats[stat], awayTeamStats[stat], mean_dict[stat], std_dev_dict[stat])
        gameAsList.append(zScoreDif)
    return [gameAsList]

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

def combine_data():
    home_path = os.getcwd()
    frames = []
    target_files = ['gamesWithInfo2010-11.csv','gamesWithInfo2011-12.csv','gamesWithInfo2012-13.csv'
    ,'gamesWithInfo2013-14.csv','gamesWithInfo2014-15.csv']
    for file in os.listdir(home_path+'/Data/OriginalData/'):
        if file in target_files:
            # newName = 'gamesWithMoreInfo' + file[-11:]
            # print(file,newName)
            df = pd.read_csv(home_path+'/Data/OriginalData/'+file)
            # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            frames.append(df)
            # df.to_csv(home_path+'/Data/t'+file)

    allGames = pd.concat(frames)
    allGames.to_csv(home_path+'/Data/OriginalData/COMBINEDgamesWithInfo2010-15.csv')

def reverse_data():
    for file in os.listdir(home_path+'/Data/MoreInfoData/'):
        

        if 'COMBINED' in file:
            all_games = pd.read_csv(home_path+'/Data/MoreInfoData/'+file)
            print(all_games)
            new_games = all_games.copy()
            features = ['W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
            'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
            'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE','Result']
            for index, game in all_games.iterrows():
                for feature in features:
                    if feature == 'Result':
                        result = game['Result']
                        if result == 0:
                            new_games.at[index,'Result'] = '1'
                        else:
                            new_games.at[index,'Result'] = '0'
                    else:
                        if game[feature] != 0:
                            new_games.at[index,feature] = float(game[feature]) * -1
                # Flip teams
                temp = game['Away']
                new_games.at[index,'Away'] = game['Home']
                new_games.at[index,'Home'] = temp
            frames = [all_games,new_games]
            new_data_set = pd.concat(frames)
            new_data_set.to_csv(home_path+'/Data/MoreInfoData/NEWgamesWithInfo2010-15.csv')
                    

def main():
    reverse_data()

if __name__ == "__main__":
	main()