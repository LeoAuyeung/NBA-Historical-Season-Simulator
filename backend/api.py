import time
from flask import Flask
from flask import request
from flask import jsonify
import json


from utils import get_team_stats, get_game_schedule_list, create_game_dict, set_directory


#from AI_algorithms import predict

#from predict import dummy_function
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

	print('teamsAndSeasons',teamsAndSeasons)

	#Frontend is expecting an array with dicts inside
	#Example: [{'teamName': 'Golden State Warriors', 'wins': 73, 'losses': 9, 'wlPercent': 0.89}, {'name': 'John', 'age': 30, 'city': 'New York'}]
	#We will need to take the standings list from predict.py and turn it into that ^^^ then return it to frontend
	
	'''
	model_name = "model_knn_20200518"
	home_team = {
		"season": "2015-16",
		"name": "Boston Celtics"
	}
	away_season = "2015-16"
	'''
	set_directory("SavedModels")
	model_name = "model_random_forest_20200519160613"

	home_team = {
		"season": teamsAndSeasons[3],
		"name": teamsAndSeasons[2]
	}
	away_season = teamsAndSeasons[1]


	#predict_season(home_team, away_season, model_name, use_cached_stats = True, save_to_CSV = False)
	#response_json = json.dumps(predict_season(home_team, away_season, model_name, use_cached_stats = True, save_to_CSV = False) )
	#return { 'predictions' : predict_season}
	#response_json = jsonify(predict_season(home_team, away_season, model_name, use_cached_stats = True, save_to_CSV = False) )

	#print('response_json',response_json);
	prediction_list = predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = False, use_game_date = False);
	#print('prediction_list', prediction_list)

	#predict_season result is being turned into a string. we want it to stay as a list fuck

	#return {'listOfPredictions': response_json};
	return jsonify({"listOfPredictions": prediction_list})

'''
		win_or_loss = 'Win';
		if (game_with_prediction[1][0].item() == 1):
			win_or_loss = 'Loss'

Put this in predicts.py so it will display win or loss
'''


#dummy_function(); A test to see if we can import a function from predict.py

#-------------------- TESTING FRONTEND SENDING TO BACKEND WITH TEAM SELECTION
#dummy_function();


'''
teamsAndSeasons = ["Atlanta Hawks", "2019-20", "Los Angeles Lakers", "2018-19"]


model_name = "model_random_forest_20200519160613"
home_team = {
	"season": teamsAndSeasons[3],
	"name": teamsAndSeasons[2]
}
away_season = teamsAndSeasons[1]

print('works');

#print('response_json',response_json);
#before predict_season(home_team, away_season, model_name, use_cached_stats = True, save_to_CSV = False, use_game_date = True)
predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = True, use_game_date = True)
'''

'''
set_directory("SavedModels")

# INPUTS USED TO PREDICT SEASON
model_name = "model_random_forest_20200519160613"
home_team = {
	"season": "2017-18",
	"name": "Los Angeles Lakers"
}
away_season = "2017-18"

predict_season(home_team, away_season, model_name, use_cached_stats = False, save_to_CSV = False, use_game_date = False)
'''

'''
Reference:

Build a Simple CRUD App with Python, Flask, and React
- https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react

Parse JSON - Convert from JSON to Python
- https://www.w3schools.com/python/python_json.asp

Flask example with POST
- https://stackoverflow.com/questions/22947905/flask-example-with-post
- https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
- https://stackoverflow.com/questions/10999990/get-raw-post-body-in-python-flask-regardless-of-content-type-header/23898949

Convert Python List Into Dict
- https://appdividend.com/2019/11/12/how-to-convert-python-list-to-dictionary-example/
'''