import pickle
import pandas as pd

from process import createMeanStandardDeviationDicts, zScoreDifferential
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import setCurrentWorkingDirectory, getStatsForTeam

def gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startDate, endDate, season):

	homeTeam, awayTeam = list(game.items())[0]
	gameAsList = [homeTeam, awayTeam]

	homeTeamStats = getStatsForTeam(homeTeam, startDate, endDate, season)
	awayTeamStats = getStatsForTeam(awayTeam, startDate, endDate, season)

	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		zScoreDif = zScoreDifferential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
		gameAsList.append(zScoreDif)
	
	return [gameAsList]

def predictGame(game, modelName, currentDate, season, startOfSeason):
	
	meanDict, standardDeviationDict = createMeanStandardDeviationDicts(startOfSeason, currentDate, season)
	gameAsList = gameWithZScoreDifsList(game, meanDict, standardDeviationDict, startOfSeason, currentDate, season)
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
	prediction = pickleModel.predict_proba(justZScoreDifs)

	gameWithPrediction = [game, prediction]
	return gameWithPrediction

def interpretPrediction(gameWithPrediction):

	game, prediction = gameWithPrediction

	winProb = prediction[0][1]
	winProbRounded = round(winProb, 4)
	# Formulates percent chance that home team wins
	winProbPercent = "{:.2%}".format(winProbRounded)

	homeTeam = list(game.keys())[0]
	awayTeam = list(game.values())[0]

	print('There is a ' + winProbPercent + ' chance that the ' + homeTeam + ' will defeat the ' + awayTeam + '.')

def main():
	setCurrentWorkingDirectory('SavedModels')
	game = {'Los Angeles Clippers': 'Memphis Grizzlies'}
	gameWithPrediction = predictGame(game, "model_20200512", '01-04-2020', '2019-20', '10-22-2019')
	interpretPrediction(gameWithPrediction)


if __name__ == "__main__":
	main()