import time
from flask import Flask
from flask import request
from flask import jsonify
import json

from predict import predict_season

app = Flask(__name__)

#Test call to check if frontend can call backend
@app.route('/time')
def get_current_time():
	return {'time': time.time()}

# Run predict.py and return the standings back to frontend
@app.route('/standings', methods = ['POST'])
def get_standings():
	data = json.loads(request.data)
	teamsAndSeasons = data['teamList'] #Holds Ex: ['Chicago Bulls', '2019-20', 'Atlanta Hawks', '2019-20']

	model_name = "final_model"
	home_team = {
		"season": teamsAndSeasons[3],
		"name": teamsAndSeasons[2]
	}
	away_season = teamsAndSeasons[1]

	if teamsAndSeasons[3] == "2015-16" and teamsAndSeasons[2] == "Chicago Bulls" and teamsAndSeasons[1] == "2018-19":
		demo = True
	else:
		demo = False

	prediction_list = predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = True, use_game_date = True, demo = demo);

	return jsonify({"listOfPredictions": prediction_list})