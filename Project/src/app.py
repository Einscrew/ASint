#!/usr/bin/env python3
from flask import Flask, Response, abort, render_template, request, jsonify, redirect
from itertools import chain
import db

from functools import wraps

from random import randint
import requests
import json

app = Flask(__name__)
app.config.from_pyfile('settings')

db = db.Db()

with open("../keys.json",'r') as f:
	FENIX_API = json.load(f)
	
FENIX_API['redirectURI']= 'http://127.0.0.1:5000/messages'


def validAdmin(username, password):
    return username == app.config['USER'] and password == app.config['PASS']

def admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth.username or not auth.password or not validAdmin(auth.username, auth.password):
            return Response('Credentials required!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        return f(*args, **kwargs)
    return wrapper

'''ADMIN ENDPOINTS'''
#Manage Buildings
@app.route('/API/admin/building/manage',methods=['PUT'])
@admin
def buildingsManagement():
	buildingList = []
	''' File containing buildings'''

	if request.is_json:
		buildingList = request.get_json()
	else:
		for i in request.form:
			for line in i.split('\n'):
				buildingList.add({"_id": ID, "name": name, "location": { "lat": lat, "lon": lon }})
	db.insertBuildings(buildingList)
	return "done"

#Logged Users
@app.route('/API/admin/users/loggedin', methods=['POST'])
@admin
def listLoggedUsers():
	users = db.getAllLoggedUsers()
	for user in users:
		print(user)

#Logged Users In building
@app.route('/API/admin/building/<string:buildingID>/users', methods=['POST'])
@admin
def listUsersInBuilding(buildingID):
	return str(buildingID)

#History
@app.route('/API/admin/logs', methods=['POST'])
@admin
def history():
	return "hello"+request.url

#history by building
@app.route('/API/admin/building/<string:buildingID>/logs', methods=['POST'])
def historyByBuilding(buildingID):
	#Movements in building
	return 'by building'
	buildingMoves = db.getBuildingMovements(buildingID)
	#Messages in building
	buildingMessages = db.getBuildingMessages(buildingID)

	logs = sorted([l for l in chain(buildingMoves, buildingMessages)], key=lambda k: k['time'])
	for log in logs:
		print(log)

	return str(logs)

#history by user
@app.route('/API/admin/users/<string:istID>/logs', methods=['POST'])
def historyByUser(istID):
	return 'by user'
	#User movements
	userMovements = getUserMovements(istID)
	#User messages
	userMessages = getUserMessages(istID)

	logs = sorted([l for l in chain(userMovements, userMessages)], key=lambda k: k['time'])
	for log in logs:
		print(log)

	return str(logs)

#create new bot
@app.route('/API/admin/bot/create/<string:buildingID>', methods=['PUT'])
def newBot(buildingID):
	r = db.insertBot(buildingID)
	return jsonify( { 'key':r, 'building':buildingID})


'''USER ENDPOINTS'''
@app.route('/API/login/', methods=['POST'])
def fenixLogin():
	return jsonify({"istID":'2iwi2kd'})
	#User(1234)
	#fenixURL = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(FENIX_API['clientID'])+'&redirect_uri='+FENIX_API['redirectURI']
	#redirect(fenixURL)

#Send Message
@app.route('/API/users/<string:istID>/message', methods=['POST'])
def sendMsg(istID):
	try:
		print(request.is_json)
		d = request.get_json()
		return str(db.insertMessage(istID, db.getUsersInRange(istID), d['message'], {'lat':d['lat'],'lon':d['lon']}, None))
	except:
		abort(json(message="something went wrong"))
	return "ok"

#Set Range
@app.route('/API/users/<string:istID>/range/#range',methods=['PUT'])
def setRange(istID):
	pass

#List users in range
@app.route('/API/users/<string:istID>/range')
def range(istID):
	pass

#List users in range
@app.route('/API/users/<string:istID>/message/received', methods=['POST'])
def received(istID):
	return jsonify(db.getUserMessages(istID))

'''BOTS ENDPOINTS'''



#@app.route('/')
#def hello_world():
#	url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(FENIX_API['clientID'])+'&redirect_uri='+FENIX_API['redirectURI']
#	return render_template("mainPage.html", url=url)

@app.route('/')
def hello_world():
	istID = 'ist' + str(randint(150000, 200000))
	if db.insertUser(istID, {'lat':12,'lon':241}, 9):
		return render_template("webApp.html", istID=istID)
	else:
		abort(jsonify(message="user already registered???"))

@app.route('/logout')
def logout(istID):
	db.removeUser(istID)
	#Here redirect to login page again
	#return render_template("webApp.html", istID)


@app.route('/messages')
def messages():

	# get code provided by fenixedu
	code = request.args.get('code')
	access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
	request_data = {'client_id': int(FENIX_API['clientID']), 'client_secret': FENIX_API['clientSecret'],
			'redirect_uri': FENIX_API['redirectURI'], 'code': code, 'grant_type': 'authorization_code'}

	request_access_token = requests.post(access_token_request_url, data=request_data)

	access_token = request_access_token.json()['access_token']
	refresh_token = request_access_token.json()['refresh_token']
	token_expires =  request_access_token.json()['expires_in']

	params = {'access_token': access_token}
	request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)

	print(request_info.json())
	return "<p>yeyy</p>"#render_template("messages.html")

if __name__ == '__main__':
	app.run()
