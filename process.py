from nba_api.stats.endpoints import leaguedashteamstats
import statistics
import time
from constants import HEADERS, STATS_TYPE

# Finds league stats for entered basic or advanced statistic (statType = 'Base' or 'Advanced')
def basicOrAdvancedStat(startDate, endDate, season='2018-19', statType='Base'):

    time.sleep(.5)

     # Gets list of dictionaries with stats for every team
    allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                        measure_type_detailed_defense=statType,
                                                        date_from_nullable=startDate,
                                                        date_to_nullable=endDate,
                                                        season=season,
                                                        headers=HEADERS,
                                                        timeout=120)
    allTeamsDict = allTeamsInfo.get_normalized_dict()
    
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