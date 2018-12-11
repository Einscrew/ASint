import requests
import json
URL ='http://127.0.0.1:5000'

def setbuildings(file):
	with open(file, 'r') as f:
		build = json.load(f)
	return requests.put(URL+'/API/admin/building/manage', json=build, auth=('user', 'pass'))

def LoggedUsers(buildingID=None):

	if buildingID is None:
		endpoint='/API/admin/users/loggedin'
	else:
		endpoint='/API/admin/building/'+str(buildingID)+'/users'

	return requests.post(URL+endpoint, auth=('user', 'pass'))

def Logs(filters= None):
	if not filters or "user" not in filters and "building" not in filters:
		endpoint='/API/admin/logs'
	elif "user" in filters:
		endpoint='/API/admin/users/'+str(filters["user"])+'/logs'	
	elif "building" in filters:
		endpoint='/API/admin/building/'+str(filters["building"])+'/logs'

	return requests.post(URL+endpoint, auth=('user', 'pass'))

def createBot():
	pass


if __name__ == '__main__':
	while(True):
		print(eval(input('>>')))