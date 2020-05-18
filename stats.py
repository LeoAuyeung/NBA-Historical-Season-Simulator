from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

nba_teams = teams.get_teams()
# # Select the dictionary for the Celtics, which contains their team ID.
celtics = [team for team in nba_teams if team['abbreviation'] == 'BOS'][0]
celtics_id = celtics['id']

# # print(celtics_id)s

# # Query for games where the Celtics were playing.
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=celtics_id)
# # The first DataFrame of those returned is what we want.
games = gamefinder.get_data_frames()[0]
games.head()

# Subset the games to when the last 4 digits of SEASON_ID were 2017.

games_1718 = games[games.SEASON_ID.str[-4:] == '2017']
games_1718.head()

# Prints the DataFrame object from pandas library.
print(games_1718)