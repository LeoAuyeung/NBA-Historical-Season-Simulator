import pickle
import pandas as pd
from timeit import default_timer as timer
from datetime import datetime

from process import createMeanStandardDeviationDicts, zScoreDifferential
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import setCurrentWorkingDirectory, getStatsForTeam, getSeasonDates

def gameWithZScoreDifsList(homeTeam, awayTeam, meanDict, standardDeviationDict, useCachedStats=False):

	gameAsList = [homeTeam["label"], awayTeam["label"]]

	homeTeamStats = getStatsForTeam(homeTeam["name"], homeTeam["startDate"], homeTeam["endDate"], homeTeam["season"], useCachedStats)
	awayTeamStats = getStatsForTeam(awayTeam["name"], awayTeam["startDate"], awayTeam["endDate"], awayTeam["season"], useCachedStats)

	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
		gameAsList.append(zScoreDif)
	
	return [gameAsList]

def predictGame(game, modelName, useCachedStats=False):

	base_season = game["away"]["season"]
	base_season_startDate = game["away"]["startDate"]
	base_season_endDate = game["away"]["endDate"]

	# given home team is swapped team, create mean and stddev using away team season
	meanDict, standardDeviationDict = createMeanStandardDeviationDicts(base_season_startDate, base_season_endDate, base_season)
	gameAsList = gameWithZScoreDifsList(game["home"], game["away"], meanDict, standardDeviationDict, useCachedStats)

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

def interpretPrediction(gameWithPrediction):
	# teams = gameWithPrediction["teams"]
	# prediction = gameWithPrediction["prediction"]
	# matchDate = gameWithPrediction["date"]

	game, prediction = gameWithPrediction

	homeTeam = game["home"]
	awayTeam = game["away"]

	prediction = prediction[0].item()

	if prediction == 0:
		winner = homeTeam
	elif prediction == 1:
		winner = awayTeam

	print(f'{homeTeam["label"]} vs. {awayTeam["label"]} : {winner["label"]}')

def createGameDict(homeTeam, awayTeam):

	home_season = homeTeam["season"]
	home_season_dates = getSeasonDates(home_season)
	home_startDate = home_season_dates["start"]
	home_endDate = home_season_dates["end"]

	homeTeam["startDate"] = home_startDate
	homeTeam["endDate"] = home_endDate
	homeTeam["label"] = homeTeam["season"] + " " + homeTeam["name"]


def predictSeason(homeTeam, awaySeason, modelName, useCachedStats=False, saveToCSV=True):
	matchScheduleList = getGameScheduleList(homeTeam, awaySeason)

	awayTeam["startDate"] = away_startDate
	awayTeam["endDate"] = away_endDate
	awayTeam["label"] = awayTeam["season"] + " " + awayTeam["name"]

	for index, match in enumerate(matchScheduleList):
		awayTeam = {
			"season": awaySeason,
			"name": match["awayTeam"],
		}

		game = createGameDict(homeTeam, awayTeam)
		gameWithPrediction = predictGame(game, modelName, useCachedStats)

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

		now = datetime.now()
		now_str = now.strftime("%Y%m%d")

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


# home team is the swapped team
def main():
	setCurrentWorkingDirectory('SavedModels')
	modelName = "model_dTree_20200518"

	homeTeam = {
		"season": "2019-20",
		"name": "Los Angeles Clippers"
	}
	awaySeason = "2015-16"

	predictSeason(homeTeam, awaySeason, modelName, useCachedStats=True)

	modelName = "model_dTree_20200517"

	gameWithPrediction = predictGame(game, modelName, useCachedStats=True)
	interpretPrediction(gameWithPrediction)

if __name__ == "__main__":
	main()