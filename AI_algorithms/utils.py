import os
import time
import json
import pickle
import pandas as pd

from datetime import datetime
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats, leaguegamefinder
from constants import TEAMS, TEAMS_ABV, HEADERS, SEASON_DATES, STATS_TYPE

home_path = os.getcwd()

# Save the API call with the given parameters
def save_api_call(filename, all_teams):
    with open(home_path + '/SavedAPICalls/' + filename, 'wb') as handle:
        pickle.dump(all_teams, handle)

# Check if we've already made an API call with the given parameters.
def check_api_call(filename):
    file_found = False
    for file in os.listdir(home_path + '/SavedAPICalls/'):
        if filename in file:
            return True

    return file_found

# Get the result of the API call we've already made
def get_api_call(filename):
    with open(home_path + '/SavedAPICalls/' + filename, 'rb') as handle:
        return pickle.loads(handle.read())

def get_team_stats_2(team, startDate, endDate, season='2019-20'):
	filename = team + '_' + startDate + '_' + endDate + '_' + season + '.json'

	# Check if we've made the same api call before
	callAlreadyMade = check_api_call(filename)
	if callAlreadyMade:
		# Get the result of the API call
		allStats = get_api_call(filename)
	else:
		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
		generalTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=TEAMS[team], 
																				per_mode_detailed='Per100Possessions', 
																				date_from_nullable=startDate, 
																				date_to_nullable=endDate, 
																				season=season, 
																				headers=HEADERS, 
																				timeout=120)
		generalTeamDict = generalTeamInfo.get_normalized_dict()
		generalTeamDashboard = generalTeamDict['OverallTeamDashboard'][0]
	
		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
		advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=TEAMS[team], 
																				measure_type_detailed_defense='Advanced',
																				date_from_nullable=startDate, 
																				date_to_nullable=endDate, 
																				season=season, 
																				headers=HEADERS, 
																				timeout=120)
		advancedTeamDict = advancedTeamInfo.get_normalized_dict()
		advancedTeamDashboard = advancedTeamDict['OverallTeamDashboard'][0]

		allStats = {}
		for stat, statType in STATS_TYPE.items():
			if statType == 'Base':
				allStats[stat] = generalTeamDashboard[stat]

		for stat, statType in STATS_TYPE.items():
			if statType == 'Advanced':
				allStats[stat] = advancedTeamDashboard[stat]
		
		save_api_call(filename, allStats)
	return allStats


def get_team_stats(team, start_date, end_date, season, use_cached_stats = False, cached_filename = "2009-2019_TeamStats.csv"):
	filename = team + '_' + start_date + '_' + end_date + '_' + season + '.json'

	if use_cached_stats:
		# set directory to Data
		prog_directory = os.path.dirname(os.path.abspath(__file__))
		new_directory = os.path.join(prog_directory, "Data")
		os.chdir(new_directory)

		# read csv
		all_stats = pd.read_csv(cached_filename)
		headers = list(all_stats)[2:]

		# get team stats
		team_stats = all_stats.loc[(all_stats['season'] == season) & (all_stats['team'] == team)]

		all_stats  = {}
		for h in headers:
			all_stats[h] = team_stats[h].values[0]
		
		# set directory to SavedModels
		prog_directory = os.path.dirname(os.path.abspath(__file__))
		new_directory = os.path.join(prog_directory, "SavedModels")
		os.chdir(new_directory)

	else:
		time.sleep(1)
		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
		general_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = TEAMS[team], per_mode_detailed = 'Per100Possessions', date_from_nullable = start_date, date_to_nullable = end_date, season = season, headers = HEADERS, timeout = 60)

		general_team_dict = general_team_info.get_normalized_dict()
		general_team_dash = general_team_dict['OverallTeamDashboard'][0]

		# Uses NBA_API to access the dictionary holding advanced stats for every team
		adv_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = TEAMS[team], measure_type_detailed_defense = 'Advanced', date_from_nullable = start_date, date_to_nullable = end_date, season = season, headers = HEADERS, timeout = 120)
		adv_team_dict = adv_team_info.get_normalized_dict()
		adv_team_dash = adv_team_dict['OverallTeamDashboard'][0]

		all_stats = {}
		for stat, stat_type in STATS_TYPE.items():
			if stat_type == 'Base':
				all_stats[stat] = general_team_dash[stat]

		for stat, stat_type in STATS_TYPE.items():
			if stat_type == 'Advanced':
				all_stats[stat] = adv_team_dash[stat]

	return all_stats

def create_game_dict(home_team, away_team):

	# Setting necessary variables to create the home and away team dictionaries
	home_season = home_team["season"]
	home_season_dates = get_season_dates(home_season)

	home_team["start_date"] = home_season_dates["start"]
	home_team["end_date"] = home_season_dates["end"]
	home_team["label"] = home_team["season"] + " " + home_team["name"]

	away_season = away_team["season"]
	away_season_dates = get_season_dates(away_season)

	away_team["start_date"] = away_season_dates["start"]
	away_team["end_date"] = away_season_dates["end"]
	away_team["label"] = away_team["season"] + " " + away_team["name"]

	return {
		"home": home_team,
		"away": away_team
	}

# Get the season dates
def get_season_dates(season):
	if season in SEASON_DATES:
		return SEASON_DATES[season]

# Create_nba_season_dates_dict(2008, 2018) for 2008-09 to 2018-19
def create_nba_season_dates_dict(first, last):
	seasons = {}
	
	for x in range(first, last + 1):
		season_str = f'{x}-{str(x+1)[-2:]}'

		season_dates = get_season_dates(season_str)

		seasons[season_str] = season_dates

	return seasons

# Create the actual CSVs of the stats
def create_team_stats_csv():
	# set directory to Data
	prog_directory = os.path.dirname(os.path.abspath(__file__))
	new_directory = os.path.join(prog_directory, "Data")
	os.chdir(new_directory)

	all_stats = []
	# for each season, get dates
	for season in SEASON_DATES.keys():
		dates = get_season_dates(season)
		start_date = dates["start"]
		end_date = dates["end"]

		# for each team, get stats of that season
		for team in TEAMS:
			stats = get_team_stats(team, start_date, end_date, season)
			stats["team"] = team
			stats["season"] = season

			print(stats)

			all_stats.append(stats)

	# feature cols we are using
	columns = ["season", "team", "W_PCT", "REB", "TOV", "PLUS_MINUS", "OFF_RATING", "DEF_RATING", "TS_PCT"]
	df = pd.DataFrame(all_stats, columns = columns)

	df.to_csv("2009-2019_TeamStats.csv", index = False)

# Get the entire schedule of a team during a specific season
def get_game_schedule_list(home_team, away_season):
	# Set necessary variables
	home_team_name = home_team["name"]
	team_id = TEAMS[home_team_name]
	dates = SEASON_DATES[away_season]
	start = datetime.strptime(dates["start"], "%m/%d/%Y").strftime("%Y-%m-%d")
	end = datetime.strptime(dates["end"], "%m/%d/%Y").strftime("%Y-%m-%d")

	# use the NBA api endpoint to find the game
	gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_id, season_nullable = away_season)
	games = gamefinder.get_data_frames()[0]

	# Get the regular season games that we need from the specified dates
	regular_season_games_df = games.loc[(games["GAME_DATE"] >= start) & (games["GAME_DATE"] <= end)].sort_values("GAME_DATE")
	regular_season_games_list = regular_season_games_df.to_dict("records")
	regular_season_games = []

	# For each game in regular season, we want to add the new team
	for game in regular_season_games_list:
		match = game["MATCHUP"]
		split_vs = match.split(" vs. ")
		if len(split_vs) == 1:
			split_at = match.split(" @ ")
			split = split_at
		else:
			split = split_vs
		away_team = split[1]
		away_team_name = TEAMS_ABV[away_team]

		date_df = game["GAME_DATE"]
		date_str = datetime.strptime(date_df, "%Y-%m-%d").strftime("%m/%d/%Y")

		actual = game["WL"]
		if actual == "W":
			actual_encoded = 0
		elif actual == "L":
			actual_encoded = 1

		game_dict = {
			"season" : away_season,
			"away_team" : away_team_name,
			"date": date_str,
			"actual": actual_encoded
		}
		regular_season_games.append(game_dict)
	
	return regular_season_games

def parsePredictionCSV(filename):
	# set directory to Predictions
	prog_directory = os.path.dirname(os.path.abspath(__file__))
	new_directory = os.path.join(prog_directory, "Predictions")
	os.chdir(new_directory)

	with open(filename) as f:
		predicitons = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace = True)]
	
	return predicitons

def getStatsForPredictionsCSV(predictions):
	num_matches = len(predictions)

	predicted_losses = sum([int(g["prediction"]) for g in predictions])
	predictied_wins = num_matches - predicted_losses
	
	actual_losses = sum([int(g["actual"]) for g in predictions])
	actual_wins = num_matches - actual_losses

	wrong_preditions = sum([1 for x in predictions if x["prediction"] != x["actual"]])
	right_preditions = num_matches - wrong_preditions

	stats = {
		"num_matches": num_matches,
		"predicted_losses": predicted_losses,
		"predicted_wins": predictied_wins,
		"actual_losses": actual_losses,
		"actual_wins": actual_wins,
		"wrong_preditions": wrong_preditions,
		"right_preditions": right_preditions
	}

	print(stats)

# getStatsForPredictionsCSV(parsePredictionCSV("2015-16-Boston Celtics_2015-16_model_knn_20200518_20200518185052_predictions.csv"))