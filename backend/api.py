import time
from flask import Flask
from flask import request
import json

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


	return {'test': 'test'}

'''
Reference:

Build a Simple CRUD App with Python, Flask, and React
- https://developer.okta.com/blog/2018/12/20/crud-app-with-python-flask-react

Parse JSON - Convert from JSON to Python
- https://www.w3schools.com/python/python_json.asp

'''