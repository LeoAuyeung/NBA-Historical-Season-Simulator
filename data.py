import pickle
import pandas as pd

from nba_api.stats.endpoints import leaguegamelog

from process import createMeanStandardDeviationDicts, zScoreDifferential
from nba_api.stats.library.parameters import SeasonTypeAllStar
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import setCurrentWorkingDirectory, getStatsForTeam

import os
home_path = os.getcwd()

def gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startDate, endDate, season):
    homeTeam, awayTeam = list(game.items())[0]
    gameAsList = [homeTeam, awayTeam]
    homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate, season)
    awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate, season)
    
    for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
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
		columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV','PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	)

    return gameWithZScoreDifs

def main():
    # Whichever year we want the data for.
    # seasonYear = 2015
    gamefinder = leaguegamelog.LeagueGameLog(season=seasonYear, season_type_all_star=SeasonTypeAllStar.default)
    games = gamefinder.get_data_frames()[0]
    prevTeam = games['TEAM_NAME'][0]
    startOfSeason = games['GAME_DATE'][0]
    season = startOfSeason[:4] + '-' + str(int(startOfSeason[2:4])+1)

    # If for some reason your program stopped running, continue progress by 
    # settiing this to the last index that was downloaded.
    # !!! When -1, it will reset whatever file you were saving to so be careful !!!
    lastIndexDownloaded = -1
    # For a given season, iterate through all the games
    for index, row in games.iterrows():
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

            percentageDone = (index + 1) / (games.shape[0]/2) # Total number of games
            percentageDone *= 100
            print('['+str(index)+'] Progress: ' + str(round(percentageDone, 3)) + '%', " | ", game, gameDate)

            if index == 1:
                # Initialize the file with headers. This function resets the file.
                gameStat.to_csv(home_path+'/Data/gamesWithInfo' + season + '.csv')
            else:
                with open(home_path+'/Data/gamesWithInfo' + season + '.csv','a') as file:
                    gameStat.to_csv(file, header=False)
        else:
            prevTeam = row['TEAM_NAME']

if __name__ == "__main__":
	main()