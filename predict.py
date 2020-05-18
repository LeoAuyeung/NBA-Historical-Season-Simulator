import os
import pickle
import pandas as pd
from timeit import default_timer as timer

from process import create_mean_std_dev_dicts, z_score_difference
from constants import TEAMS, STATS_TYPE, HEADERS
from utils import get_team_stats, get_game_schedule_list, create_game_dict

# Get the normalized Z-scores of the games played based on the home and away team stats, mean, and std dev
def get_z_scores_list(home_team, away_team, mean_dict, std_dev_dict, use_cached_stats=False):

	games = [home_team["label"], away_team["label"]]

	home_stats = get_team_stats(home_team["name"], home_team["start_date"], home_team["end_date"], home_team["season"], use_cached_stats)
	away_stats = get_team_stats(away_team["name"], away_team["start_date"], away_team["end_date"], away_team["season"], use_cached_stats)

	for stat, statType in STATS_TYPE.items():  # Finds Z Score Dif for stats listed above and adds them to list
		z_score_dif = z_score_difference(home_stats[stat], away_stats[stat], mean_dict[stat], std_dev_dict[stat])
		games.append(z_score_dif)
	
	return [games]

# Predict the game based on the training model used. Can use a cached training model.
def predict_game(game, model_name, use_cached_stats=False):

	base_season = game["away"]["season"]
	base_season_startDate = game["away"]["start_date"]
	base_season_endDate = game["away"]["end_date"]

	# given home team is swapped team, create mean and stddev using away team season
	mean_dict, std_dev_dict = create_mean_std_dev_dicts(base_season_startDate, base_season_endDate, base_season)
	games = get_z_scores_list(game["home"], game["away"], mean_dict, std_dev_dict, use_cached_stats)

	# Pandas dataframe holding daily games and Z-Score differentials between teams
	game_with_z_score_difs = pd.DataFrame(
		games,
		columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV','PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
	)

	# Slices only the features used in the model
	just_z_score_difs = game_with_z_score_difs.loc[:, 'W_PCT':'TS_PCT']

	with open(f'{model_name}.pkl', 'rb') as file:
		pickleModel = pickle.load(file)

	# Predicts the probability that the home team loses/wins
	prediction = pickleModel.predict(just_z_score_difs)

	game_with_prediction = [game, prediction]
	return game_with_prediction

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

# Predict an entire season using the original team's schedule
def predict_season(home_team, away_season, model_name, use_cached_stats=False, saveToCSV=True):
	match_schedule_list = get_game_schedule_list(home_team, away_season)

	games_df = []

	# for each match in the schedule
	for index, match in enumerate(match_schedule_list):
		away_team = {
			"season": away_season,
			"name": match["away_team"],
		}

		game = create_game_dict(home_team, away_team)
		game_with_prediction = predict_game(game, model_name, use_cached_stats=True)

		result = {
			"teams" : game_with_prediction[0],
			"prediction": game_with_prediction[1],
			"date": match["date"]
		}
		interpret_prediction(result, unit="season", index=index+1)

		result_df = {
			"home": game_with_prediction[0]["home"]["name"],
			"away": game_with_prediction[0]["away"]["name"],
			"date": match["date"],
			"prediction": game_with_prediction[1][0].item(),
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

		df.to_csv(f'{home_team["season"]}-{home_team["name"]}_{away_season}_predictions.csv', index=False)

		# set directory to SavedModels
		prog_directory = os.path.dirname(os.path.abspath(__file__))
		new_directory = os.path.join(prog_directory, "SavedModels")
		os.chdir(new_directory)
	
	num_matches = len(match_schedule_list)

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

	# INPUTS USED TO PREDICT SEASON
	model_name = "model_dTree_20200517"
	home_team = {
		"season": "2015-16",
		"name": "Boston Celtics"
	}
	away_season = "2018-19"

	predict_season(home_team, away_season, model_name, use_cached_stats=True)

	end = timer() 

	elapsed_time = end - start
	print(f'Elapsed Time: {int(elapsed_time / 60)} minutes {int(elapsed_time % 60)} seconds.')

if __name__ == "__main__":
	main()