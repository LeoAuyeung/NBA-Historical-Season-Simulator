TEAMS = {
    "Atlanta Hawks": 1610612737,
    "Boston Celtics":1610612738,
    "Brooklyn Nets": 1610612751,
    "Charlotte Hornets": 1610612766,
    "Charlotte Bobcats": 1610612766,
    "Chicago Bulls": 1610612741,
    "Cleveland Cavaliers": 1610612739,
    "Dallas Mavericks": 1610612742,
    "Denver Nuggets": 1610612743,
    "Detroit Pistons": 1610612765,
    "Golden State Warriors": 1610612744,
    "Houston Rockets": 1610612745,
    "Indiana Pacers": 1610612754,
    "LA Clippers": 1610612746,
    "Los Angeles Clippers": 1610612746,
    "Los Angeles Lakers": 1610612747,
    "Memphis Grizzlies": 1610612763,
    "Miami Heat": 1610612748,
    "Milwaukee Bucks": 1610612749,
    "Minnesota Timberwolves": 1610612750,
    "New Jersey Nets": 1610612751,
    "New Orleans Hornets": 1610612740,
    "New Orleans Pelicans": 1610612740,
    "New York Knicks": 1610612752,
    "Oklahoma City Thunder": 1610612760,
    "Orlando Magic": 1610612753,
    "Philadelphia 76ers": 1610612755,
    "Phoenix Suns": 1610612756,
    "Portland Trail Blazers": 1610612757,
    "Sacramento Kings": 1610612758,
    "San Antonio Spurs": 1610612759,
    "Toronto Raptors": 1610612761,
    "Utah Jazz": 1610612762,
    "Washington Wizards": 1610612764,
}

TEAMS_ABV = {
   "ATL":"Atlanta Hawks",
   "BOS":"Boston Celtics",
   "BKN":"Brooklyn Nets",
   "CHA":"Charlotte Hornets",
   "CHB":"Charlotte Bobcats",
   "CHI":"Chicago Bulls",
   "CLE":"Cleveland Cavaliers",
   "DAL":"Dallas Mavericks",
   "DEN":"Denver Nuggets",
   "DET":"Detroit Pistons",
   "GSW":"Golden State Warriors",
   "HOU":"Houston Rockets",
   "IND":"Indiana Pacers",
   "LAC":"Los Angeles Clippers",
   "LAL":"Los Angeles Lakers",
   "MEM":"Memphis Grizzlies",
   "MIA":"Miami Heat",
   "MIL":"Milwaukee Bucks",
   "MIN":"Minnesota Timberwolves",
   "NOP":"New Orleans Pelicans",
   "NYK":"New York Knicks",
   "OKC":"Oklahoma City Thunder",
   "ORL":"Orlando Magic",
   "PHI":"Philadelphia 76ers",
   "PHX":"Phoenix Suns",
   "POR":"Portland Trail Blazers",
   "SAC":"Sacramento Kings",
   "SAS":"San Antonio Spurs",
   "TOR":"Toronto Raptors",
   "UTA":"Utah Jazz",
   "WAS":"Washington Wizards"
}

HEADERS = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://stats.nba.com/',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
}

# STATS_TYPE = {
#     'W_PCT':'Base',
#     'REB':'Base',
#     'TOV':'Base',
#     'PLUS_MINUS':'Base',
#     'OFF_RATING':'Advanced',
#     'DEF_RATING':'Advanced',
#     'TS_PCT':'Advanced'
# }

# Feature importance
STATS_TYPE = {
   'W_PCT':'Base',
   'NET_RATING':'Advanced',
   'PLUS_MINUS':'Base',
   'PIE':'Advanced',
   'E_NET_RATING':'Advanced',
   'DEF_RATING':'Advanced',
   'E_OFF_RATING':'Advanced',
   'OFF_RATING':'Advanced',
   'PTS':'Base',
   'TS_PCT':'Advanced',
}

# K-best
# STATS_TYPE = {
#    'W_PCT':'Base',
#    'NET_RATING':'Advanced',
#    'PLUS_MINUS':'Base',
#    'E_NET_RATING':'Advanced',
#    'PIE':'Advanced',
#    'E_OFF_RATING':'Advanced',
#    'PTS':'Base',
#    'OFF_RATING':'Advanced',
#    'TS_PCT':'Advanced',
#    'E_DEF_RATING':'Advanced',
# }

ADDITIONAL_STATS_TYPE = {
    'W_PCT':'Base',
    'MIN':'Base',
    'FGM':'Base',
    'FGA':'Base',
    'FG_PCT':'Base',
    'FG3M':'Base',
    'FG3A':'Base',
    'FG3_PCT':'Base',
    'FTM':'Base',
    'FTA':'Base',
    'FT_PCT':'Base',
    'OREB':'Base',
    'DREB':'Base',
    'REB':'Base',
    'AST':'Base',
    'TOV':'Base',
    'STL':'Base',
    'BLK':'Base',
    'BLKA':'Base',
    'PF':'Base',
    'PFD':'Base',
    'PTS':'Base',
    'PLUS_MINUS':'Base',
    'E_OFF_RATING':'Advanced',
    'OFF_RATING':'Advanced',
    'E_DEF_RATING':'Advanced',
    'DEF_RATING':'Advanced',
    'E_NET_RATING':'Advanced',
    'NET_RATING':'Advanced',
    'AST_PCT':'Advanced',
    'AST_TO':'Advanced',
    'AST_RATIO':'Advanced',
    'OREB_PCT':'Advanced',
    'DREB_PCT':'Advanced',
    'REB_PCT':'Advanced',
    'TM_TOV_PCT':'Advanced',
    'EFG_PCT':'Advanced',
    'TS_PCT':'Advanced',
    'E_PACE':'Advanced',
    'PACE':'Advanced',
    'PACE_PER40':'Advanced',
    'POSS':'Advanced',
    'PIE':'Advanced',
}

SEASON_DATES = {
   "2008-09":{
      "start":"10/28/2008",
      "end":"04/16/2009"
   },
   "2009-10":{
      "start":"10/27/2009",
      "end":"04/14/2010"
   },
   "2010-11":{
      "start":"10/26/2010",
      "end":"04/13/2011"
   },
   "2011-12":{
      "start":"12/25/2011",
      "end":"04/26/2012"
   },
   "2012-13":{
      "start":"10/30/2012",
      "end":"04/17/2013"
   },
   "2013-14":{
      "start":"10/29/2013",
      "end":"04/16/2014"
   },
   "2014-15":{
      "start":"10/28/2014",
      "end":"04/15/2015"
   },
   "2015-16":{
      "start":"10/27/2015",
      "end":"04/13/2016"
   },
   "2016-17":{
      "start":"10/25/2016",
      "end":"04/12/2017"
   },
   "2017-18":{
      "start":"10/17/2017",
      "end":"04/11/2018"
   },
   "2018-19":{
      "start":"10/16/2018",
      "end":"04/10/2019"
   },
   "2019-20":{
      "start":"10/22/2019",
      "end":"3/11/2020"
   }
}