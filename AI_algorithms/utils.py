import os
import time
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats

from constants import TEAMS, HEADERS, ADDITIONAL_STATS_TYPE

import json
import pickle

home_path = os.getcwd()

# Save the API call with the given parameters
def saveAPICall(filename, allStats):
    with open(home_path+'/SavedAPICalls/'+filename, 'wb') as handle:
        pickle.dump(allStats, handle)

# # Save the API call with the given parameters
# def saveAPICall(filename, allTeamsDict):
#     with open(home_path+'/SavedAPICalls/'+filename, 'wb') as handle:
#         pickle.dump(allTeamsDict, handle)

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
		

def getStatsForTeam(team, startDate, endDate, season='2019-20'):
	filename = team + '_' + startDate + '_' + endDate + '_' + season + '.json'

	# Check if we've made the same api call before
	callAlreadyMade = checkAPICall(filename)
	if callAlreadyMade:
		# Get the result of the API call
		allStats = getAPICall(filename)
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
		for stat, statType in ADDITIONAL_STATS_TYPE.items():
			if statType == 'Base':
				allStats[stat] = generalTeamDashboard[stat]

		for stat, statType in ADDITIONAL_STATS_TYPE.items():
			if statType == 'Advanced':
				allStats[stat] = advancedTeamDashboard[stat]
		
		saveAPICall(filename, allStats)
	return allStats

# def getStatsForTeam(team, startDate, endDate, season='2019-20'):
# 	filename = team + '_' + startDate + '_' + endDate + '_' + season + 'Per100Possessions.json'

# 	# Check if we've made the same api call before
# 	callAlreadyMade = checkAPICall(filename)
# 	if callAlreadyMade:
# 		# Get the result of the API call
# 		generalTeamDict = getAPICall(filename)
# 	else:
# 		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
# 		generalTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=TEAMS[team], 
# 																				per_mode_detailed='Per100Possessions', 
# 																				date_from_nullable=startDate, 
# 																				date_to_nullable=endDate, 
# 																				season=season, 
# 																				headers=HEADERS, 
# 																				timeout=120)
# 		generalTeamDict = generalTeamInfo.get_normalized_dict()
# 		saveAPICall(filename, generalTeamDict)
# 	generalTeamDashboard = generalTeamDict['OverallTeamDashboard'][0]

# 	allStats = {}
# 	# Returns Win PCT, Rebounds, Turnovers, and Plus Minus
# 	for stat, statType in ADDITIONAL_STATS_TYPE.items():
# 		if statType == 'Base':
# 			allStats[stat] = generalTeamDashboard[stat]
	
# 	filename = team + '_' + startDate + '_' + endDate + '_' + season + 'Advanced.json'
	
# 	# Check if we've made the same api call before
# 	callAlreadyMade = checkAPICall(filename)
# 	if callAlreadyMade:
# 		# Get the result of the API call
# 		advancedTeamDict = getAPICall(filename)
# 	else:
# 		# Uses NBA_API to access the dictionary holding basic stats for every team per 100 possessions
# 		advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=TEAMS[team], 
# 																				measure_type_detailed_defense='Advanced',
# 																				date_from_nullable=startDate, 
# 																				date_to_nullable=endDate, 
# 																				season=season, 
# 																				headers=HEADERS, 
# 																				timeout=120)
# 		advancedTeamDict = advancedTeamInfo.get_normalized_dict()
# 		saveAPICall(filename, advancedTeamDict)
# 	advancedTeamDashboard = advancedTeamDict['OverallTeamDashboard'][0]

# 	# Variables holding OFF Rating, DEF Rating, and TS%

# 	for stat, statType in ADDITIONAL_STATS_TYPE.items():
# 		if statType == 'Advanced':
# 			allStats[stat] = advancedTeamDashboard[stat]

# 	return allStats

# Sets current working directory relative to where program folder is located
def setCurrentWorkingDirectory(directoryName):

    programDirectory = os.path.dirname(os.path.abspath(__file__))
    newCurrentWorkingDirectory = os.path.join(programDirectory, directoryName)
    os.chdir(newCurrentWorkingDirectory)