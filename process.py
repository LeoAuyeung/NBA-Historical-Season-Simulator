from nba_api.stats.endpoints import leaguedashteamstats
import statistics
import time
from constants import HEADERS, STATS_TYPE

import json

import pandas as pd

import pickle

import os
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

# Finds league stats for entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basicOrAdvancedStat(startDate, endDate, season='2018-19', statType='Base'):
    time.sleep(.2)
    
    filename = statType + '_' + startDate + '_' + endDate + '_' + season + '.json'

    # Check if we've made the same api call before
    callAlreadyMade = checkAPICall(filename)

    if callAlreadyMade:
        # Get the result of the API call
        allTeamsDict = getAPICall(filename)
    else:
        # Gets list of dictionaries with stats for every team
        allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                            measure_type_detailed_defense=statType,
                                                            date_from_nullable=startDate,
                                                            date_to_nullable=endDate,
                                                            season=season,
                                                            headers=HEADERS,
                                                            timeout=120)
        allTeamsDict = allTeamsInfo.get_normalized_dict()
        saveAPICall(filename, allTeamsDict)
    
    allTeamsList = allTeamsDict['LeagueDashTeamStats']
    return allTeamsList

# Returns a standardized version of each data point via the z-score method
def basicOrAdvancedStatZScore(observedStat, mean, standardDeviation):

    zScore = (observedStat-mean)/standardDeviation  # Calculation for z-score

    return(zScore)

def zScoreDifferential(observedStatHome, observedStatAway, mean, standardDeviation):

    homeTeamZScore = basicOrAdvancedStatZScore(observedStatHome, mean, standardDeviation)
    awayTeamZScore = basicOrAdvancedStatZScore(observedStatAway, mean, standardDeviation)

    differenceInZScore = homeTeamZScore - awayTeamZScore
    return differenceInZScore

def createMeanStandardDeviationDicts(startDate, endDate, season):

    meanDict = {}
    standardDeviationDict = {}

    # Make API calls and store data in two variables
    allTeamsInfoBase = basicOrAdvancedStat(startDate, endDate, season, 'Base')
    allTeamsInfoAdvanced = basicOrAdvancedStat(startDate, endDate, season, 'Advanced')

    if not allTeamsInfoAdvanced or not allTeamsInfoAdvanced: # If we got no data
        return None

    # Loops through and inputs standard deviation and mean for each stat into dict
    for stat, statType in STATS_TYPE.items():
        # Choose which data to use depending on the stat type
        data = []
        if statType == 'Base':
            data = allTeamsInfoBase
        else:
            data = allTeamsInfoAdvanced
            
        # Mean
        specificStatAllTeams = []
        for i in range(len(data)):  # Loops through and appends specific stat to new list until every team's stat has been added
            specificStatAllTeams.append(data[i][stat])
        mean = statistics.mean(specificStatAllTeams)  # Finds mean of stat
        meanDict.update({stat: mean})

        # Standard deviation
        specificStatAllTeams = []
        for i in range(len(data)):  # Loops through and appends specific stat to new list until every team's stat has been added
            specificStatAllTeams.append(data[i][stat])
        standardDeviation = statistics.stdev(specificStatAllTeams)  # Finds standard deviation of stat
        standardDeviationDict.update({stat: standardDeviation})
 
    bothDicts = []
    bothDicts.append(meanDict)
    bothDicts.append(standardDeviationDict)

    return bothDicts