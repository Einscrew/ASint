#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request, jsonify, redirect

import requests
import json

app = Flask(__name__)

with open("../keys.json",'r') as f:
	FENIX_API = json.load(f)
	
FENIX_API['redirectURI']= 'http://127.0.0.1:5000/messages'


'''ADMIN ENDPOINTS'''

#Manage Buildings
@app.route('/API/admin/building/manage',methods=['PUT'])
def buildingsManagement():
	''' File containing buildings'''
	for i in request.form:
		print(i)
		for line in i.split('\n'):
			#j+=Building(line.split(','))
			j += 1
	return j

#Logged Users
@app.route('/API/admin/users/loggedin')
def listLoggedUsers():
	pass

#Logged Users In building
@app.route('/API/admin/building/<string:buildingID>/users')
def listUsersInBuilding(buildingID):
	pass

#History
@app.route('/API/admin/logs')
def history():
	pass

#history by building
@app.route('/API/admin/building/<string:buildingID>/logs/')
def historyByBuilding(buildingID):
	pass

#history by user
@app.route('/API/admin/users/<string:istID>/logs')
def historyByUser(istID):
	pass

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
	print(request.is_json)
	d= request.get_json()
	print(d)
	return 'Message Received'

#Set Range
@app.route('/API/users/<string:istID>/range/#range')
def setRange(istID,methods=['PUT']):
	pass

#List users in range
@app.route('/API/users/<string:istID>/range/')
def range(istID):
	pass

#List users in range
@app.route('/API/users/<string:istID>/message/received/')
def received(istID, methods=['POST']):
	return "Hello there\n"

'''BOTS ENDPOINTS'''



#@app.route('/')
#def hello_world():
#	url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(FENIX_API['clientID'])+'&redirect_uri='+FENIX_API['redirectURI']
#	return render_template("mainPage.html", url=url)

@app.route('/')
def hello_world():
	return render_template("webApp.html")

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
