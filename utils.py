import os
import time
import json
import pickle
import csv
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats, leaguegamefinder

import wptools
from datetime import datetime
import pandas as pd

from constants import TEAMS, HEADERS, SEASON_DATES, TEAMS_ABV

from pprint import pprint

home_path = os.getcwd()

# Save the API call with the given parameters
def saveAPICall(filename, allTeamsDict):
	with open(home_path+'/SavedAPICalls/'+filename, 'wb') as handle:
		pickle.dump(allTeamsDict, handle)

# Check if we've already made an API call with the given parameters.
def checkAPICall(filename):
	fileFound = False
	for file in os.listdir(home_path+'/SavedAPICalls/'):
		if filename in file:
			return True

	return fileFound

# Get the result of the API call we've already made
def getAPICall(filename):
	with open(home_path+'/SavedAPICalls/'+filename, 'rb') as handle:
		return pickle.loads(handle.read())


def getStatsForTeam(team, startDate, endDate, season, useCachedStats=False, cachedFileName="2009-2019_TeamStats.csv"):
	filename = team + '_' + startDate + '_' + endDate + '_' + season + '.json'

	print(startDate, endDate)

	if useCachedStats:
		setCurrentWorkingDirectory("Data")

		# read csv
		allTeamStats = pd.read_csv(cachedFileName)
		headers = list(allTeamStats)[2:]

		teamStats = allTeamStats.loc[(allTeamStats['season'] == season) & (allTeamStats['team'] == team)]

		allStats  = {}
		for h in headers:
			allStats[h] = teamStats[h].values[0]
		
		setCurrentWorkingDirectory("SavedModels")

	else:
		time.sleep(1)
		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
		generalTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
			team_id=TEAMS[team], 
			per_mode_detailed='Per100Possessions', 
			date_from_nullable=startDate, 
			date_to_nullable=endDate, 
			season=season, 
			headers=HEADERS, 
			timeout=120
		)

		generalTeamDict = generalTeamInfo.get_normalized_dict()
		generalTeamDashboard = generalTeamDict['OverallTeamDashboard'][0]

		# Returns Win PCT, Rebounds, Turnovers, and Plus Minus
		winPercentage = generalTeamDashboard['W_PCT']
		rebounds = generalTeamDashboard['REB']
		turnovers = generalTeamDashboard['TOV']
		plusMinus = generalTeamDashboard['PLUS_MINUS']

		# Uses NBA_API to access the dictionary holding advanced stats for every team
		advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
			team_id=TEAMS[team], 
			measure_type_detailed_defense='Advanced', 
			date_from_nullable=startDate, 
			date_to_nullable=endDate, 
			season=season, 
			headers=HEADERS, 
			timeout=120
		)
		advancedTeamDict  = advancedTeamInfo.get_normalized_dict()
		advancedTeamDashboard = advancedTeamDict['OverallTeamDashboard'][0]

		# Variables holding OFF Rating, DEF Rating, and TS%
		offensiveRating = advancedTeamDashboard['OFF_RATING']
		defensiveRating = advancedTeamDashboard['DEF_RATING']
		trueShootingPercentage = advancedTeamDashboard['TS_PCT']

		# Puts all the stats for specified team into a dictionary
		allStats = {
			'W_PCT':winPercentage,
			'REB':rebounds,
			'TOV':turnovers,
			'PLUS_MINUS':plusMinus,
			'OFF_RATING':offensiveRating,
			'DEF_RATING': defensiveRating,
			'TS_PCT':trueShootingPercentage,
		}

	return allStats

# Sets current working directory relative to where program folder is located
def setCurrentWorkingDirectory(directoryName):

	programDirectory = os.path.dirname(os.path.abspath(__file__))
	newCurrentWorkingDirectory = os.path.join(programDirectory, directoryName)
	os.chdir(newCurrentWorkingDirectory)

def createGameDict(homeTeam, awayTeam):

	home_season = homeTeam["season"]
	home_season_dates = getSeasonDates(home_season)
	home_startDate = home_season_dates["start"]
	home_endDate = home_season_dates["end"]

	homeTeam["startDate"] = home_startDate
	homeTeam["endDate"] = home_endDate
	homeTeam["label"] = homeTeam["season"] + " " + homeTeam["name"]


	away_season = awayTeam["season"]
	away_season_dates = getSeasonDates(away_season)
	away_startDate = away_season_dates["start"]
	away_endDate = away_season_dates["end"]

	awayTeam["startDate"] = away_startDate
	awayTeam["endDate"] = away_endDate
	awayTeam["label"] = awayTeam["season"] + " " + awayTeam["name"]

	return {
		"home": homeTeam,
		"away": awayTeam
	}


def getSeasonDates(season):
	if season in SEASON_DATES:
		return SEASON_DATES[season]
	else:
		return getNBASeasonStartEndDates(season)

def getNBASeasonStartEndDates(season):
	name = f"{season} NBA season"
	page = wptools.page(name, silent=True).get_parse(show=False)
	duration = page.data['infobox']["duration"]

	if season == "2019-20":
		split = duration.split("|")[1].split("(")[0].strip()
		start, end = split.split(" – ")
	else:
		split = duration.split("<br>")
		if len(split) == 1:
			start, end = duration.split("<br />")[0].strip().split(" – ")
		else:
			start, end = duration.split("<br>")[0].strip().split(" – ")

	date_fmt_parse = "%B %d, %Y"

	start_dt = datetime.strptime(start, date_fmt_parse)
	end_dt = datetime.strptime(end, date_fmt_parse)

	date_fmt_str = "%m/%d/%Y"

	start_str = start_dt.strftime(date_fmt_str)
	end_str = end_dt.strftime(date_fmt_str)

	return {"start": start_str, "end": end_str}


# createNBASeasonDatesDict(2008, 2018) for 2008-09 to 2018-19
def createNBASeasonDatesDict(first, last):
	seasons = {}

	for x in range(first, last + 1):
		season_str = f'{x}-{str(x+1)[-2:]}'

		season_dates = getNBASeasonStartEndDates(season_str)

		seasons[season_str] = season_dates

	print(seasons)

	return seasons


def createStatsForTeamsCSV():
	setCurrentWorkingDirectory("Data")

	allStats = []
	for season in SEASON_DATES.keys():
		dates = getSeasonDates(season)
		startDate = dates["start"]
		endDate = dates["end"]

		for team in TEAMS:
			stats = getStatsForTeam(team, startDate, endDate, season)
			stats["team"] = team
			stats["season"] = season

			print(stats)

			allStats.append(stats)

	columns = ["season", "team", "W_PCT", "REB", "TOV", "PLUS_MINUS", "OFF_RATING", "DEF_RATING", "TS_PCT"]
	df = pd.DataFrame(allStats, columns=columns)

	df.to_csv("2009-2019_TeamStats.csv", index=False)

def getGameScheduleList(homeTeam, awaySeason):
	homeTeamName = homeTeam["name"]
	team_id = TEAMS[homeTeamName]
	dates = SEASON_DATES[awaySeason]
	start = datetime.strptime(dates["start"], "%m/%d/%Y").strftime("%Y-%m-%d")
	end = datetime.strptime(dates["end"], "%m/%d/%Y").strftime("%Y-%m-%d")

	gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=awaySeason)
	games = gamefinder.get_data_frames()[0]

	regular_season_games_df = games.loc[(games["GAME_DATE"] >= start) & (games["GAME_DATE"] <= end)].sort_values("GAME_DATE")
	regular_season_games_list = regular_season_games_df.to_dict("records")
	regular_season_games = []
	for game in regular_season_games_list:
		match = game["MATCHUP"]
		split_vs = match.split(" vs. ")
		if len(split_vs) == 1:
			split_at = match.split(" @ ")
			split = split_at
		else:
			split = split_vs
		awayTeam = split[1]
		awayTeamName = TEAMS_ABV[awayTeam]

		date_df = game["GAME_DATE"]
		date_str = datetime.strptime(date_df, "%Y-%m-%d").strftime("%m/%d/%Y")

		actual = game["WL"]
		if actual == "W":
			actual_encoded = 0
		elif actual == "L":
			actual_encoded = 1

		game_dict = {
			"season" : awaySeason,
			"awayTeam" : awayTeamName,
			"date": date_str,
			"actual": actual_encoded
		}
		regular_season_games.append(game_dict)
	
	return regular_season_games

def parsePredictionCSV(filename):
	setCurrentWorkingDirectory("Predictions")

	with open(filename) as f:
		predicitons = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
	
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

	pprint(stats)


# getStatsForPredictionsCSV(parsePredictionCSV("2015-16-Boston Celtics_2015-16_model_knn_20200518_20200518185052_predictions.csv"))