#!/usr/bin/env python3
from flask import Flask, Response, abort, make_response, render_template, request, jsonify, redirect, url_for
from itertools import chain
import db

from werkzeug.contrib.cache import SimpleCache

from functools import wraps

from random import randint
import requests
import json

import datetime

app = Flask(__name__)
app.config.from_pyfile('settings')

cache = SimpleCache()

db = db.Db()

with open("../keys.json",'r') as f:
	APP = json.load(f)


with open("../secret", 'rb') as f:
	app.secret_key = f.read()


APP['redirectURI'] = 'http://127.0.0.1:5000/'
APP['loginURI'] = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(APP['clientID'])+'&redirect_uri='+APP['redirectURI']

@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

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

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		cookie = request.cookies.get('access_token')
		print('COOKIE IN REQUEST?:', cookie)
		if cookie == None or cookie != cache.get('access_token'):#or 'username' not in session:#c is None:
			cache.clear()
			request.get('https://id.tecnico.ulisboa.pt/cas/logout')
			return redirect(APP['loginURI'])
		if cache.get('username') not in kwargs.values(): #and cookie != session['username']:
			cache.clear()
			return abort(401)#redirect('/login',302)#Response('Credentials required!', 302, {'WWW-Authenticate': 'Basic realm="Login!"','Location':'http://127.0.0.1:5000/'})
			#return Response(make_response('/login'), 302)#APP['loginURI'])

		return f(*args, **kwargs)
	return decorated_function

'''ADMIN ENDPOINTS'''
#Manage Buildings
@app.route('/API/admin/buildings/manage',methods=['PUT'])
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


@app.route('/API/admin/buildings',methods=['POST'])
@admin
def buildingsList():
	s = db.getBuildings()
	print(jsonify(s))
	return jsonify(s)

#Logged Users
@app.route('/API/admin/users/loggedin', methods=['POST'])
@admin
def listLoggedUsers():
	users = db.getAllLoggedUsers()
	for user in users:
		print(user)

#Logged Users In building
@app.route('/API/admin/buildings/<string:buildingID>/users', methods=['POST'])
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
def historyByBuilding(buildingID, moves=True, messages=True):
	#return 'by building'
	if moves:
		#Movements in building
		buildingMoves = db.getBuildingMovements(buildingID)
	if messages:
		#Messages in building
		buildingMessages = db.getBuildingMessages(buildingID)

	if moves and messages:
		logs = sorted([l for l in chain(buildingMoves, buildingMessages)], key=lambda k: k['time'])
	elif moves and not messages:
		logs = buildingMoves
	elif messages and not moves:
		logs = buildingMessages

	return str(logs)

#history by user
@app.route('/API/admin/users/<string:istID>/logs', methods=['POST'])
def historyByUser(istID, moves=True, messages=True):
	#return 'by user'
	if moves:
		#User movements
		userMovements = getUserMovements(istID)
	if messages:
		#User messages
		userMessages = getUserMessages(istID)

	if moves and messages:
		logs = sorted([l for l in chain(userMovements, userMessages)], key=lambda k: k['time'])
	elif moves and not messages:
		logs = userMovements
	elif messages and not moves:
		logs = userMessages

	return str(logs)

#create new bot
@app.route('/API/admin/bot/create/<string:buildingID>', methods=['PUT'])
@admin
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
@app.route('/API/users/<string:istID>/range/<int:newRange>',methods=['POST'])
def setRange(istID, newRange):
	try:
		print(request.is_json)
		d = request.get_json()
		return str(db.updateUserRange(istID, newRange))
	except:
		abort(json(message="something went wrong"))
	return "ok"	

#Update user's location
@app.route('/API/users/<string:istID>/location',methods=['POST'])
def updateLocation(istID):
	try:
		print(request.is_json)
		d = request.get_json()
		print(d)
		db.updateUserLocation(istID,{'lat': d['lat'], 'lon': d['lon']})
	except:
		abort(json(message="something went wrong"))
	return "ok"

#List users in range
@app.route('/API/users/<string:istID>/range', methods=['POST'])
def usersInRange(istID):
	try:		
		users = db.getUsersInRange(istID)
		usersInBuilding = db.getUsersInSameBuilding(istID)
		if usersInBuilding != None:
			users.union(usersInBuilding)
		s = "\n"
		seq = (u for u in users)
		return jsonify({'users': s.join(seq)})
	except:
		abort(json(message="something went wrong"))
	return "ok"

#List users in range
@app.route('/API/users/<string:istID>/message/received', methods=['POST'])
@login_required
def received(istID):
	print('COOKIE IN REQUEST?:', request.cookies.get('access_token'))
	return jsonify(db.getUserMessages(istID))

#Updates user's building
@app.route('/API/users/<string:istID>/building', methods=['POST'])
def updateBuilding(istID):
	db.getUserBuilding(istID)
	return "ok"


'''BOTS ENDPOINTS'''



#@app.route('/')
#def hello_world():
#	url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(FENIX_API['clientID'])+'&redirect_uri='+FENIX_API['redirectURI']
#	return render_template("mainPage.html", url=url)

@app.route('/')
def hello_world():
	code = request.args.get('code')
	print(cache)
	#	input('fdssss	')

	if code is None and cache.get('access_token') is None:
		return redirect(APP['loginURI'])

	elif code is not None and cache.get('access_token') is None:
		cache.add('username',getUserInfo(code),timeout = 5)
		return redirect('/')
	
	db.insertUser(cache.get('username'), {'lat':12,'lon':241}, 10)
	resp = make_response(render_template("webApp.html", istID=cache.get('username')))

	resp.set_cookie('access_token', cache.get('access_token'))#, expires=(datetime.datetime.now()+datetime.timedelta(seconds=30)))	
	return resp

@app.route('/logout')
def logout(istID):
	db.removeUser(istID)
	#Here redirect to login page again
	#return render_template("webApp.html", istID)

@app.route('/login')
def log():
	return render_template("mainPage.html")


def getUserInfo(code):
    access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
    request_data = {'client_id': int(APP['clientID']), 'client_secret': APP['clientSecret'],
            'redirect_uri': APP['redirectURI'], 'code': code, 'grant_type': 'authorization_code'}

    reqAccessToken = requests.post(access_token_request_url, data=request_data)

    token = reqAccessToken.json().get('access_token')
    cache.add('access_token', token, timeout=5)
    print('access token in cache',cache.get('access_token'))


    request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params={'access_token': token})
    return request_info.json().get('username')

if __name__ == '__main__':
	app.run()
