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


	return {['Chicago Bulls', 60, 20, '75%']}

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

'''