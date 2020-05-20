from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

from datetime import datetime
from constants import SEASON_DATES, TEAMS, TEAMS_ABV
from pprint import pprint

team = "Boston Celtics"
team_id = TEAMS[team]

season = "2018-19"
dates = SEASON_DATES[season]
start = datetime.strptime(dates["start"], "%m/%d/%Y").strftime("%Y-%m-%d")
end = datetime.strptime(dates["end"], "%m/%d/%Y").strftime("%Y-%m-%d")

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season)
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

    game_dict = {
        "season" : season,
        "name" : awayTeamName,
        "date": date_str
    }
    regular_season_games.append(game_dict)

pprint(regular_season_games)
