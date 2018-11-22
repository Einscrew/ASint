#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
import json

app = Flask(__name__)

FENIX_API = json.load(open("../keys.json",'r'))
FENIX_API['redirectURI']= 'http://127.0.0.1:5000/messages'

@app.route('/')
def hello_world():
	url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(FENIX_API['clientID'])+'&redirect_uri='+FENIX_API['redirectURI']
	return render_template("mainPage.html", url=url)

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
