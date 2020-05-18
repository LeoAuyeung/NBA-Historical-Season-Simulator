import os
import time
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats

import wptools
from datetime import datetime

from constants import TEAMS, HEADERS, SEASON_DATES

def getStatsForTeam(team, startDate, endDate, season='2019-20'):

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
	advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=TEAMS[team], measure_type_detailed_defense='Advanced', date_from_nullable=startDate, date_to_nullable=endDate, season=season, headers=HEADERS, timeout=120)
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
