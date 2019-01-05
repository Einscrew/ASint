#!/usr/bin/env python3
import requests
import json
URL ='http://127.0.0.1:5000'


def SetBuildings(file='buildings.json'):
	try:
		with open(file, 'r') as f:
			build = json.load(f)
	except:
		return 'error'
	return requests.put(URL+'/API/admin/buildings/manage', json=build, auth=('user', 'pass'))


def LoggedUsers(filters=None):
	if filters is None:
		endpoint='/API/admin/users/loggedin'
		r = requests.post(URL+endpoint, auth=('user', 'pass'))
		return r.content if r.status_code == 200 else None
	else:
		s = set()
		for f in filters:
			endpoint='/API/admin/buildings/'+f+'/users'
			r = requests.post(URL+endpoint, auth=('user', 'pass'))
			if r.status_code == 200:
				s = s.union(set(r.json().get('users')))
		return s
		
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
		d = dict()
		num = 1
		for b in buildings:
			d[num] = b['_id']
			print('{:3} {}'.format(num, b['name']))
			num = num+1
		num = input('Type the number(s) of the building(s) to associate with (separated by ,): ')

		num = num.split(',')
		
		if len(num) > 0:
			try:
				data = [d[int(n)] for n in num]
				data = ','.join(data)
				print(requests.put(URL+'/API/admin/bot/create', data = {'buildings':data}, auth=('user', 'pass')).content)
			except KeyError:
				print("Error on input")
	else:
		print("Error occour")



def getBuilding():
	if input(">> By building [y|Y]: ") in ['y','Y']:
		resp = requests.post(URL+'/API/admin/buildings', auth=('user','pass'))
		if resp.status_code == 200 and 'application/json' in resp.headers['Content-Type']:
			buildings = resp.json()
			d = dict()
			num = 1
			for b in buildings:
				d[num] = b['_id']
				print('{:3} {}'.format(num, b['name']))
				num = num+1

			num = input('\nType the number(s) of the building(s) to see their active users: ')
			
			r = [d[int(n)] for n in num.split(',')]
			print(r)
			return r

	return None


if __name__ == '__main__':
	while(True):
		print('''
1 - setup buildings
2 - logged in users
3 - logs
4 - create bot''')
		try:
			i = int(input('>>'))
			if i == 1:
				SetBuildings()
			elif i == 2:
				print(LoggedUsers(filters=getBuilding()))
			elif i == 3:
				i = input('Logs [raw, user, building]?')
				f = None
				if i == "user" or i == "building":
					f = dict()
					f[i] = input(i+ "number: ")
				Logs(filters = f)
			elif i == 4:
				createBot()

		except TypeError:
			pass