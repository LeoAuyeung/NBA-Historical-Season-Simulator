import pickle
import pandas as pd
from timeit import default_timer as timer
from datetime import datetime

from process import createMeanStandardDeviationDicts, zScoreDifferential
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import setCurrentWorkingDirectory, getStatsForTeam, getSeasonDates, getGameScheduleList, createGameDict

def gameWithZScoreDifsList(homeTeam, awayTeam, meanDict, standardDeviationDict, useCachedStats=False, useGameDate=False, gameDate=None):

	gameAsList = [homeTeam["label"], awayTeam["label"]]

	homeTeamStats = getStatsForTeam(homeTeam["name"], homeTeam["startDate"], gameDate, homeTeam["season"], useCachedStats)
	if useGameDate:
		awayTeamStats = getStatsForTeam(awayTeam["name"], awayTeam["startDate"], gameDate, awayTeam["season"], useCachedStats)
	else:
		awayTeamStats = getStatsForTeam(awayTeam["name"], awayTeam["startDate"], awayTeam["endDate"], awayTeam["season"], useCachedStats)

	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
		gameAsList.append(zScoreDif)
	
	return [gameAsList]

def predictGame(game, modelName, useCachedStats=False, useGameDate=False, gameDate=None):

	base_season = game["away"]["season"]
	base_season_startDate = game["away"]["startDate"]
	base_season_endDate = game["away"]["endDate"]

	# given home team is swapped team, create mean and stddev using away team season
	if useGameDate:
		meanDict, standardDeviationDict = createMeanStandardDeviationDicts(base_season_startDate, gameDate, base_season)
	else:
		meanDict, standardDeviationDict = createMeanStandardDeviationDicts(base_season_startDate, base_season_endDate, base_season)

	gameAsList = gameWithZScoreDifsList(game["home"], game["away"], meanDict, standardDeviationDict, useCachedStats, useGameDate, gameDate)

	# Pandas dataframe holding daily games and Z-Score differentials between teams
	gameWithZScoreDifs = pd.DataFrame(
		gameAsList,
		columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV','PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	)

	# Slices only the features used in the model
	justZScoreDifs = gameWithZScoreDifs.loc[:, 'W_PCT':'TS_PCT']

	with open(f'{modelName}.pkl', 'rb') as file:
		pickleModel = pickle.load(file)

	# Predicts the probability that the home team loses/wins
	prediction = pickleModel.predict(justZScoreDifs)

	gameWithPrediction = [game, prediction]
	return gameWithPrediction

def predictSeason(homeTeam, awaySeason, modelName, useCachedStats=False, saveToCSV=False, useGameDate=False):
	matchScheduleList = getGameScheduleList(homeTeam, awaySeason)

	games_df = []

	for index, match in enumerate(matchScheduleList):
		awayTeam = {
			"season": awaySeason,
			"name": match["awayTeam"],
		}

		game = createGameDict(homeTeam, awayTeam)
		gameWithPrediction = predictGame(game, modelName, useCachedStats, useGameDate, match["date"])

		result = {
			"teams" : gameWithPrediction[0],
			"prediction": gameWithPrediction[1],
			"date": match["date"]
		}
		interpretPrediction(result, unit="season", index=index+1)

		result_df = {
			"home": gameWithPrediction[0]["home"]["name"],
			"away": gameWithPrediction[0]["away"]["name"],
			"date": match["date"],
			"prediction": gameWithPrediction[1][0].item(),
			"actual": match["actual"]
		}
		games_df.append(result_df)
	
	if saveToCSV:
		columns = ["date", "home", "away", "prediction", "actual"]
		df = pd.DataFrame(games_df, columns=columns)

		setCurrentWorkingDirectory('Predictions')

		df.to_csv(f'{homeTeam["season"]}-{homeTeam["name"]}_{awaySeason}_{modelName}_{now_str}_predictions.csv', index=False)

		setCurrentWorkingDirectory('SavedModels')
	
	num_matches = len(matchScheduleList)

	predicted_losses = sum([int(g["prediction"]) for g in games_df])
	predictied_wins = num_matches - predicted_losses
	
	actual_losses = sum([int(g["actual"]) for g in games_df])
	actual_wins = num_matches - actual_losses

	return {
		"num_matches": num_matches,
		"predicted_losses": predicted_losses,
		"predicted_wins": predictied_wins,
		"actual_losses": actual_losses,
		"actual_wins": actual_wins
	}


def interpretPrediction(gameWithPrediction, unit, index):
	if unit == "season":
		teams = gameWithPrediction["teams"]
		prediction = gameWithPrediction["prediction"]
		matchDate = gameWithPrediction["date"]

		homeTeam = teams["home"]
		awayTeam = teams["away"]

		prediction = prediction[0].item()

		if prediction == 0:
			winner = homeTeam
		elif prediction == 1:
			winner = awayTeam

		print(f'({index}) {matchDate} - {homeTeam["label"]} vs. {awayTeam["label"]} : {winner["label"]}')

	elif unit == "game":
		game, prediction = gameWithPrediction

		homeTeam = game["home"]
		awayTeam = game["away"]

		prediction = prediction[0].item()

		if prediction == 0:
			winner = homeTeam
		elif prediction == 1:
			winner = awayTeam

		print(f'{homeTeam["label"]} vs. {awayTeam["label"]} : {winner["label"]}')

# home team is the swapped team
def main():
	start = timer()

	setCurrentWorkingDirectory('SavedModels')
	modelName = "model_knn_20200517"

	homeTeam = {
		"season": "2015-16",
		"name": "Boston Celtics"
	}
	awaySeason = "2015-16"

	predictSeason(homeTeam, awaySeason, modelName, useCachedStats=False, saveToCSV=True, useGameDate=True)

	end = timer() 

	elapsed_time = end - start
	print(f'Elapsed Time: {int(elapsed_time / 60)} minutes {int(elapsed_time % 60)} seconds.')

if __name__ == "__main__":
	main()