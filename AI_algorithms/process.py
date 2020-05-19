import os
import time
import json
import pickle
import statistics
from constants import HEADERS, STATS_TYPE
from nba_api.stats.endpoints import leaguedashteamstats

home_path = os.getcwd()

# Save the API call with the given parameters
def save_api_call(filename, all_teams_dict):
	return None
	with open(home_path + '/SavedAPICalls/'+filename, 'wb') as handle:
		pickle.dump(all_teams_dict, handle)

# Check if we've already made an API call with the given parameters.
def check_api_call(filename):
	fileFound = False
	for file in os.listdir(home_path + '/SavedAPICalls/'):
		if filename in file:
			return True

	return fileFound

# Get the result of the API call we've already made
def get_api_call(filename):
	with open(home_path + '/SavedAPICalls/' + filename, 'rb') as handle:
		return pickle.loads(handle.read())

# Finds league stats for entered basic or advanced statistic (stat_type = 'Base' or 'Advanced')
def get_league_stats(start_date, end_date, season = '2018-19', stat_type = 'Base'):
	filename = stat_type + '_' + start_date + '_' + end_date + '_' + season + '.json'
	
	# Add time.sleep so as to not overload the API with requests and timeout
	time.sleep(.3)
	
	# Check if we've made the same api call before
	call_already_made = check_api_call(filename)

	if call_already_made:
		# Get the result of the API call
		all_teams_dict = get_api_call(filename)
	else:
		# Gets list of dictionaries with stats for every team from the nba_api endpoint
		all_teams_info = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed = 'Per100Possessions', measure_type_detailed_defense = stat_type, date_from_nullable = start_date, date_to_nullable = end_date, season = season, headers = HEADERS, timeout = 60)
		all_teams_dict = all_teams_info.get_normalized_dict()
		save_api_call(filename, all_teams_dict)
	
	all_teams_list = all_teams_dict['LeagueDashTeamStats']
	return all_teams_list

# Returns a standardized version of each data point via the z-score method
def get_z_score(observed_stat, mean, std_dev):

	z_score = (observed_stat - mean) / std_dev  # Calculation for z-score

	return(z_score)

# Get the list of the Zscore differences between the home teams and the away teams based on the mean and std dev
def z_score_difference(observed_stat_home, observedStatAway, mean, std_dev):
	return get_z_score(observed_stat_home, mean, std_dev) - get_z_score(observedStatAway, mean, std_dev)

def create_mean_std_dev_dicts(start_date, end_date, season):
	# Make API calls and store data in two variables
	all_teams_infoBase = get_league_stats(start_date, end_date, season, 'Base')
	all_teams_infoAdvanced = get_league_stats(start_date, end_date, season, 'Advanced')

	# If we got no data
	if not all_teams_infoAdvanced or not all_teams_infoAdvanced: 
		return None

	mean_dict = {}
	std_dev_dict = {}
	# Loops through and inputs standard deviation and mean for each stat into dict
	for stat, stat_type in STATS_TYPE.items():
		# Choose which data to use depending on the stat type
		data = []
		if stat_type == 'Base':
			data = all_teams_infoBase
		else:
			data = all_teams_infoAdvanced
			
		# Mean
		specific_stat_all_teams = []
		for i in range(len(data)):  # Loops through and appends specific stat to new list until every team's stat has been added
			specific_stat_all_teams.append(data[i][stat])
		mean = statistics.mean(specific_stat_all_teams)  # Finds mean of stat
		mean_dict.update({stat: mean})

		# Standard deviation
		specific_stat_all_teams = []
		for i in range(len(data)):  # Loops through and appends specific stat to new list until every team's stat has been added
			specific_stat_all_teams.append(data[i][stat])
		std_dev = statistics.stdev(specific_stat_all_teams)  # Finds standard deviation of stat
		std_dev_dict.update({stat: std_dev})
 
	# We then want to output both of the mean and std dev dictionaries
	ans = []
	ans.append(mean_dict)
	ans.append(std_dev_dict)

	return ans