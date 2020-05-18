import os
import pickle
import pandas as pd
from timeit import default_timer as timer

from process import createMeanStandardDeviationDicts, zScoreDifferential
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import get_team_stats, get_season_dates, get_game_schedule_list, create_game_dict

def gameWithZScoreDifsList(homeTeam, awayTeam, meanDict, standardDeviationDict, useCachedStats=False):

	gameAsList = [homeTeam["label"], awayTeam["label"]]

	homeTeamStats = get_team_stats(homeTeam["name"], homeTeam["startDate"], homeTeam["endDate"], homeTeam["season"], useCachedStats)
	awayTeamStats = get_team_stats(awayTeam["name"], awayTeam["startDate"], awayTeam["endDate"], awayTeam["season"], useCachedStats)

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

def predictSeason(homeTeam, awaySeason, modelName, useCachedStats=False, saveToCSV=False):
	matchScheduleList = get_game_schedule_list(homeTeam, awaySeason)

	games_df = []

	for index, match in enumerate(matchScheduleList):
		awayTeam = {
			"season": awaySeason,
			"name": match["awayTeam"],
		}

		game = create_game_dict(homeTeam, awayTeam)
		gameWithPrediction = predictGame(game, modelName)

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

		# set directory to Predictions
		prog_directory = os.path.dirname(os.path.abspath(__file__))
		new_directory = os.path.join(prog_directory, "Predictions")
		os.chdir(new_directory)

		df.to_csv(f'{homeTeam["season"]}-{homeTeam["name"]}_{awaySeason}_predictions.csv', index=False)

		# set directory to SavedModels
		prog_directory = os.path.dirname(os.path.abspath(__file__))
		new_directory = os.path.join(prog_directory, "SavedModels")
		os.chdir(new_directory)
	
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
	start = timer()
	
	# set directory to SavedModels
	prog_directory = os.path.dirname(os.path.abspath(__file__))
	new_directory = os.path.join(prog_directory, "SavedModels")
	os.chdir(new_directory)
	modelName = "model_dTree_20200517"

	homeTeam = {
		"season": "2015-16",
		"name": "Boston Celtics"
	}
	awaySeason = "2018-19"

	predictSeason(homeTeam, awaySeason, modelName, useCachedStats=True)

	end = timer() 

	elapsed_time = end - start
	print(f'Elapsed Time: {int(elapsed_time / 60)} minutes {int(elapsed_time % 60)} seconds.')

if __name__ == "__main__":
	main()