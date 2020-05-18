import pickle
import pandas as pd

from process import createMeanStandardDeviationDicts, zScoreDifferential
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import setCurrentWorkingDirectory, getStatsForTeam, getSeasonDates

def gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startDate, endDate, season):

	homeTeam, awayTeam = list(game.items())[0]
	gameAsList = [homeTeam, awayTeam]

	homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate, season)
	awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate, season)

	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
		gameAsList.append(zScoreDif)
	
	return [gameAsList]

def predictGame(game, modelName, season):

	dates = getSeasonDates(season)
	startDate = dates["start"]
	endDate = dates["end"]

	meanDict, standardDeviationDict = createMeanStandardDeviationDicts(startDate, endDate, season)
	gameAsList = 	(game, meanDict, standardDeviationDict, startDate, endDate, season)

	print(gameAsList)

	return None

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

	game, prediction = gameWithPrediction

	homeTeam = list(game.keys())[0]
	awayTeam = list(game.values())[0]

	prediction = prediction[0].item()

	if prediction == 0:
		winner = homeTeam
	elif prediction == 1:
		winner = awayTeam

	print(f'{homeTeam} vs. {awayTeam} : {winner}')

def main():
	setCurrentWorkingDirectory('SavedModels')
	game = {'Los Angeles Clippers': 'Memphis Grizzlies'}
	gameWithPrediction = predictGame(game, "model_dTree_20200517", '2019-20')
	interpretPrediction(gameWithPrediction)


if __name__ == "__main__":
	main()