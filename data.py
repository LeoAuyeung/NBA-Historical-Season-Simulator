import pickle
import pandas as pd

from nba_api.stats.endpoints import leaguegamelog

from process import createMeanStandardDeviationDicts, zScoreDifferential
from nba_api.stats.library.parameters import SeasonTypeAllStar
from constants import TEAMS, STATS_TYPE, HEADERS, ADDITIONAL_STATS_TYPE
from utils import setCurrentWorkingDirectory, getStatsForTeam

import sys

import os

home_path = os.getcwd()

def gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startDate, endDate, season):
    homeTeam, awayTeam = list(game.items())[0]
    gameAsList = [homeTeam, awayTeam]
    homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate, season)
    awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate, season)
    
    for stat, statType in ADDITIONAL_STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
        zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
        gameAsList.append(zScoreDif)
    return [gameAsList]

def getData(game, season, startOfSeason, currentDate):
    bothDicts = createMeanStandardDeviationDicts(startOfSeason, currentDate, season)
    if not bothDicts or not bothDicts[0] or not bothDicts[1]: # If we got no data
        empty = pd.DataFrame()
        return empty
    meanDict = bothDicts[0]
    standardDeviationDict = bothDicts[1]

    gameAsList = gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startOfSeason, currentDate, season)
    # Pandas dataframe holding daily games and Z-Score differentials between teams
    gameWithZScoreDifs = pd.DataFrame(
		gameAsList,
		columns=[
            'Home','Away','W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
        'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
        'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE',
        ]
		# columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV','PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	)

    return gameWithZScoreDifs

def main():
    years = [2011,2015,2016,2017,2018,2019]
    for seasonYear in years:
        # Whichever year we want the data for.
        # if len(sys.argv) < 2:
        #     print("Wrong usage")
        #     sys.exit()
        # else:
        #     seasonYear = int(sys.argv[1])
        # seasonYear = 2011
        print(seasonYear)
        gamefinder = leaguegamelog.LeagueGameLog(season=seasonYear, season_type_all_star=SeasonTypeAllStar.default)
        games = gamefinder.get_data_frames()[0]
        prevTeam = games['TEAM_NAME'][0]
        startOfSeason = games['GAME_DATE'][0]
        endofSeason = games['GAME_DATE'][games.shape[0] - 1]
        if startOfSeason[2] == '0' and startOfSeason[3] != '9':
            season = startOfSeason[:4] + '-0' + str(int(startOfSeason[2:4])+1)
        else:
            season = startOfSeason[:4] + '-' + str(int(startOfSeason[2:4])+1)
        
        # # If for some reason your program stopped running, continue progress by 
        # # settiing this to the last index that was downloaded.
        # # !!! When -1, it will reset whatever file you were saving to so be careful !!!
        # If download helper exists, get it and retrieve last index
        lastIndexDownloaded = 0
        for file in os.listdir(home_path+'/TestTrainingData/'):
            if 'DownloadHelper'+season+'.csv' in file:
                df = pd.read_csv(home_path+'/TestTrainingData/DownloadHelper'+season+'.csv')
                lastIndexDownloaded = int(df['lastIndex'])
        # For a given season, iterate through all the games
        for index, row in games.iterrows():
            if lastIndexDownloaded == -10:
                print("NEED TO SET LAST INDEX")
                sys.exit()
            if index <= lastIndexDownloaded:
                continue
            if index % 2 != 0:
                currTeam = row['TEAM_NAME']
                game = {prevTeam: currTeam}
                gameDate = row['GAME_DATE']
                gameStat = getData(game, season, startOfSeason, gameDate)
                if gameStat.empty: # If we got no data
                    continue
                winLoss = row['WL']
                if winLoss == 'W':
                    gameStat['Result'] = 0
                else:
                    gameStat['Result'] = 1

                year = gameDate[:4]
                month = gameDate[5:7]
                day = gameDate[-2:]
                newDateFormat = month + '/' + day + '/' + year
                gameStat['Date'] = newDateFormat

                percentageDone = (index + 1) / games.shape[0] # Total number of games
                percentageDone *= 100
                print('['+str(index)+'] Progress: ' + str(round(percentageDone, 2)) + '%', " | ", 'Season ' + season, prevTeam + ' vs ' + currTeam)
        
                if index == 1:
                    # Initialize the file with headers. This function resets the file.
                    gameStat.to_csv(home_path+'/TestTrainingData/gamesWithMoreInfo' + season + '.csv')
                else:
                    # Keep track of last downloaded index and season year
                    downloadHelperData = {'lastIndex' : [index]}
                    downloadHelperDF = pd.DataFrame(downloadHelperData, columns = ['lastIndex'])
                    downloadHelperDF.to_csv(home_path+'/TestTrainingData/DownloadHelper'+season+'.csv')
                    with open(home_path+'/TestTrainingData/gamesWithMoreInfo'+season+'.csv','a') as file:
                        gameStat.to_csv(file, header=False)
            else:
                prevTeam = row['TEAM_NAME']

if __name__ == "__main__":
	main()