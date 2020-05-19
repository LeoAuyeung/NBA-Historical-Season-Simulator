import os
import pickle
import pandas as pd
from timeit import default_timer as timer
from datetime import datetime
from process import create_mean_std_dev_dicts, z_score_difference
from utils import get_team_stats, get_game_schedule_list, create_game_dict, set_directory
from constants import TEAMS, STATS_TYPE, HEADERS


game_date_stats = []

# Get the normalized Z-scores of the games played based on the home and away team stats, mean, and std dev
def get_z_scores_list(home_team, away_team, mean_dict, std_dev_dict, use_cached_stats = False, use_game_date = False, game_date = None):

	games = [home_team["label"], away_team["label"]]
	home_stats = get_team_stats(home_team["name"], home_team["start_date"], home_team["end_date"], home_team["season"], use_cached_stats)
	if use_game_date:
		away_stats = get_team_stats(away_team["name"], away_team["start_date"], game_date, away_team["season"], use_cached_stats)

		temp = away_stats
		temp["team"] = away_team["label"]
		temp["date"] = game_date

		game_date_stats.append(temp)
		print(temp)
	else:
		away_stats = get_team_stats(away_team["name"], away_team["start_date"], away_team["end_date"], away_team["season"], use_cached_stats)


	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		z_score_dif = z_score_difference(home_stats[stat], away_stats[stat], mean_dict[stat], std_dev_dict[stat])
		games.append(z_score_dif)
	
	return [games]

# Interpret our predicted game result
def interpret_prediction(game_with_prediction, unit, index):
	if unit == "season":
		teams = game_with_prediction["teams"]
		prediction = game_with_prediction["prediction"]
		match_date = game_with_prediction["date"]

		home_team = teams["home"]
		away_team = teams["away"]

		prediction = prediction[0].item()

		if prediction == 0:
			winner = home_team
		elif prediction == 1:
			winner = away_team

		print(f'({index}) {match_date} - {home_team["label"]} vs. {away_team["label"]} : {winner["label"]}')

	elif unit == "game":
		game, prediction = game_with_prediction

		home_team = game["home"]
		away_team = game["away"]

		prediction = prediction[0].item()

		if prediction == 0:
			winner = home_team
		elif prediction == 1:
			winner = away_team

		print(f'{home_team["label"]} vs. {away_team["label"]} : {winner["label"]}')


'''
True = 0 (Home Win)
False = 1 (Home Loss)
Actual, Prediction
TP = 0, 0
FP = 1, 0
FN = 0, 1
TN = 1, 1

	TP FP
	FN TN
'''
def interpret_prediction_season(games_df):
	total = len(games_df)
	tp = sum([1 for x in games_df if x["actual"] == x["prediction"] and x["actual"] == 0 and x["prediction"] == 0 ])
	fp = sum([1 for x in games_df if x["actual"] != x["prediction"] and x["actual"] == 1 and x["prediction"] == 0 ])
	fn = sum([1 for x in games_df if x["actual"] != x["prediction"] and x["actual"] == 0 and x["prediction"] == 1 ])
	tn = sum([1 for x in games_df if x["actual"] == x["prediction"] and x["actual"] == 1 and x["prediction"] == 1 ])

	accuracy = (tp + tn) / total
	precision = tp / (tp + fp)
	recall = tp / (tp + fn)

	# Printing accuracy, precision, and recall based on metrics data
	print('\n----------------------------------')
	print("Accuracy: ", accuracy)
	print("Precision: ", precision)
	print("Recall: ", recall)
	print('----------------------------------\n')

	# Print confusion matrix
	print("[ ", tp, fp)
	print("  ", fn, tn, " ]")
	print('----------------------------------\n')

# Predict the game based on the training model used. Can use a cached training model.
def predict_game(game, model_name, use_cached_stats = False, use_game_date = False, game_date = None):

	base_season = game["away"]["season"]
	base_season_start_date = game["away"]["start_date"]
	base_season_end_date = game["away"]["end_date"]

	# given home team is swapped team, create mean and stddev using away team season
	if use_game_date:
		mean_dict, std_dev_dict = create_mean_std_dev_dicts(base_season_start_date, game_date, base_season)
	else:
		mean_dict, std_dev_dict = create_mean_std_dev_dicts(base_season_start_date, base_season_end_date, base_season)

	games = get_z_scores_list(game["home"], game["away"], mean_dict, std_dev_dict, use_cached_stats, use_game_date, game_date)

	# Pandas dataframe holding daily games and Z-Score differentials between teams
	game_with_z_score_difs = pd.DataFrame(
		games,
		columns = ['Home', 'Away', 'W_PCT', 'REB', 'TOV','PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	)

	# Slices only the features used in the model
	just_z_score_difs = game_with_z_score_difs.loc[:, 'W_PCT':'TS_PCT']

	with open(f'{model_name}.pkl', 'rb') as file:
		pickle_model = pickle.load(file)

	# Predicts the probability that the home team loses/wins
	prediction = pickle_model.predict(just_z_score_difs)

	game_with_prediction = [game, prediction]
	return game_with_prediction


# Predict an entire season using the original team's schedule
def predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = True, use_game_date = False):
	'''
	Predicts an NBA season given a team and a season
	Uses specified model
	use_cached_stats - uses cached results from getStatsForTeam
	save_to_CSV - saves simulated results to csv
	use_game_date - for getStatsForTeam, uses match date as endDate rather than just endDate of the season
	'''
	match_schedule_list = get_game_schedule_list(home_team, away_season)

	games_df = []

	# for each match in the schedule
	for index, match in enumerate(match_schedule_list):
		away_team = {
			"season": away_season,
			"name": match["away_team"],
		}

		# create the game dictionary
		game = create_game_dict(home_team, away_team)
		# use game dictionary and given params to create predictions
		game_with_prediction = predict_game(game, model_name, use_cached_stats, use_game_date, match["date"])

		# interpret the predictions
		result = {
			"teams" : game_with_prediction[0],
			"prediction": game_with_prediction[1],
			"date": match["date"]
		}
		interpret_prediction(result, unit = "season", index = index+1)

		result_df = {
			"home": game_with_prediction[0]["home"]["name"],
			"away": game_with_prediction[0]["away"]["name"],
			"date": match["date"],
			"prediction": game_with_prediction[1][0].item(),
			"actual": match["actual"]
		}
		games_df.append(result_df)
	
	if save_to_CSV:
		now = datetime.now()
		now_str = now.strftime("%Y%m%d%H%M%S")

		columns = ["date", "home", "away", "prediction", "actual"]
		df = pd.DataFrame(games_df, columns = columns)

		# set directory to Predictions
		set_directory("Predictions")

		# save to CSV file
		df.to_csv(f'{home_team["season"]}-{home_team["name"]}_{away_season}_{model_name}_{now_str}_predictions.csv', index = False)

		# set directory to SavedModels
		set_directory("SavedModels")
	
	interpret_prediction_season(games_df)

	return games_df

# home team is the swapped team
def main():
	start = timer()
	
	# set directory to SavedModels
	set_directory("SavedModels")

	# INPUTS USED TO PREDICT SEASON
	model_name = "model_majority_20200519142646"
	home_team = {
		"season": "2008-09",
		"name": "Los Angeles Lakers"
	}
	away_season = "2008-09"

	predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = True, use_game_date = True)

	end = timer() 

	elapsed_time = end - start
	print(f'Elapsed Time: {int(elapsed_time / 60)} minutes {int(elapsed_time % 60)} seconds.')

	columns = ["team", "date", 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	df = pd.DataFrame(game_date_stats)
	set_directory("Data")
	df.to_csv("teamStats3.csv", index=False)


# if __name__ == "__main__":
# 	main()

main()