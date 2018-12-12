#!/usr/bin/env python3
import requests
import json
URL ='http://127.0.0.1:5000'

def SetBuildings(file):
	with open(file, 'r') as f:
		build = json.load(f)

	return requests.put(URL+'/API/admin/buildings/manage', json=build, auth=('user', 'pass'))


def LoggedUsers(buildingID=None):
	if buildingID is None:
		endpoint='/API/admin/users/loggedin'
	else:
		endpoint='/API/admin/buildings/'+str(buildingID)+'/users'
	return requests.post(URL+endpoint, auth=('user', 'pass'))


def Logs(filters= None):
	if not filters or "user" not in filters and "building" not in filters:
		endpoint='/API/admin/logs'
	elif "user" in filters:
		endpoint='/API/admin/users/'+str(filters["user"])+'/logs'	
	elif "building" in filters:
		endpoint='/API/admin/buildings/'+str(filters["building"])+'/logs'
	return requests.post(URL+endpoint, auth=('user', 'pass'))


def createBot():
	resp = requests.post(URL+'/API/admin/buildings', auth=('user','pass'))
	if resp.status_code == 200 and 'application/json' in resp.headers['Content-Type']:
		buildings = resp.json()
		for b in buildings:
			print(b['name'])
			
		return requests.put(URL+'/API/admin/bot/create/'+str(buildingID), auth=('user', 'pass'))
	else:
		return "Error occour"


if __name__ == '__main__':
	while(True):
		print(eval(input('>>')))