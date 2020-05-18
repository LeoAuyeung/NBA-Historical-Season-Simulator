from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import teamyearbyyearstats

import pandas as pd

from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats, teamdashboardbygamesplits

from nba_api.stats.library.parameters import Direction, LeagueID, PlayerOrTeamAbbreviation, Season, SeasonTypeAllStar, Sorter

nba_teams = teams.get_teams()
# # Select the dictionary for the Celtics, which contains their team ID.
celtics = [team for team in nba_teams if team['abbreviation'] == 'BOS'][0]
celtics_id = celtics['id']

# # print(celtics_id)s

# # Query for games where the Celtics were playing.
# gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=celtics_id)
# # The first DataFrame of those returned is what we want.
# games = gamefinder.get_data_frames()[0]
# games.head()

# # print(games)

# # Subset the games to when the last 4 digits of SEASON_ID were 2017.

# games_1718 = games[games.SEASON_ID.str[-4:] == '1990']
# games_1718.head()

# # Prints the DataFrame object from pandas library.
# # print(games_1718)
# # Prints the json form of the DataFrame object.
# # print(games_1718.to_json())

# # Query for year by year stats for Celtics.
# statsfinder = teamyearbyyearstats.TeamYearByYearStats(team_id=celtics_id)
# stats = statsfinder.get_data_frames()[0]
# stats.head()

# # Subset the games to when the year is 2017.
# stats_1718 = stats[stats.YEAR.str[2:4] == '17']
# stats_1718.head()

# # Prints the DataFrame object from pandas library.
# # print(stats_1718)
# # Prints the json form of the DataFrame object.
# # print(stats_1718.to_json())

# frames = []

# for season in range(2016,2021):
#     gamefinder = leaguegamelog.LeagueGameLog(season=season, season_type_all_star=SeasonTypeAllStar.regular)
#     frames.append(gamefinder.get_data_frames()[0])


# result = pd.concat(frames)
# print(result)


gamefinder = leaguegamelog.LeagueGameLog(season=2016, season_type_all_star=SeasonTypeAllStar.regular)
games = gamefinder.get_data_frames()[0]
print(games)



# allPairsExist = True
# prevTeam = games['TEAM_ABBREVIATION'][0]

# for index, row in games.iterrows():
#     # Get the last 3 characters: opponent team abbreviation
#     if index % 2 != 0:
#         allPairsExist = prevTeam == row['MATCHUP'][-3:]
#         if not allPairsExist:
#             print(row['TEAM_ABBREVIATION'], row['MATCHUP'][-3:])
    # prevTeam = row['TEAM_ABBREVIATION']
    # print(row['TEAM_ABBREVIATION'], row['TEAM_NAME'], row['MATCHUP'], row['WL'], row['REB'], row['TOV'], row['PLUS_MINUS'])

# # Query for games where the Celtics were playing.
# gamefinder = leaguegamefinder.LeagueGameFinder(game_id_nullable='0021600001')
# # The first DataFrame of those returned is what we want.
# games = gamefinder.get_data_frames()[0]
# games.head()
# print(games)

# result.to_csv('results.csv')

# allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
#                                                            date_from_nullable='01/01/1990',
#                                                            date_to_nullable='05/16/2020',
#                                                            timeout=120,)

# allTeamsDataFrame = allTeamsInfo.get_data_frames()[0]
# allTeamsDataFrame.head()
# print(allTeamsDataFrame)


# generalTeamInfo = leaguedashteamstats.LeagueDashTeamStats(season='2018-19',per_mode_detailed='Per100Possessions',date_from_nullable='01/01/1990',date_to_nullable='10/22/2019')
# generalTeamDict = generalTeamInfo.get_normalized_dict()
# generalTeamDashboard = generalTeamDict['OverallTeamDashboard'][0]
# print(generalTeamDashboard)

# winPercentage = generalTeamDashboard['W_PCT']
# rebounds = generalTeamDashboard['REB']
# turnovers = generalTeamDashboard['TOV']
# plusMinus = generalTeamDashboard['PLUS_MINUS']


# # Uses NBA_API to access the dictionary holding advanced stats for every team
# advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(measure_type_detailed_defense='Advanced', season='2018-19', per_mode_detailed='Per100Possessions',)
# advancedTeamDict  = advancedTeamInfo.get_normalized_dict()
# advancedTeamDashboard = advancedTeamDict['OverallTeamDashboard'][0]

# # Variables holding OFF Rating, DEF Rating, and TS%
# offensiveRating = advancedTeamDashboard['OFF_RATING']
# defensiveRating = advancedTeamDashboard['DEF_RATING']
# trueShootingPercentage = advancedTeamDashboard['TS_PCT']

# Puts all the stats for specified team into a dictionary
# allStats = {
#     # 'W_PCT':winPercentage,
#     # 'REB':rebounds,
#     # 'TOV':turnovers,
#     # 'PLUS_MINUS':plusMinus,
#     'OFF_RATING':offensiveRating,
#     'DEF_RATING': defensiveRating,
#     'TS_PCT':trueShootingPercentage,
# }
# print(allStats)

generalTeamInfo = teamdashboardbygamesplits.TeamDashboardByGameSplits(measure_type_detailed_defense='Advanced', per_mode_detailed='Per100Possessions', team_id=celtics_id, season='2010-11')
generalTeamDict = generalTeamInfo.get_normalized_dict()
generalTeamDashboard = generalTeamDict['OverallTeamDashboard']

print(generalTeamDashboard)
