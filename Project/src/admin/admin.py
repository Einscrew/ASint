#!/usr/bin/env python3
import requests
import json
#URL = 'https://asint-2018.appspot.com'
URL = 'http://127.0.0.1:5000'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def SetBuildings(file='buildings.json'):
	try:
		with open(file, 'r') as f:
			build = json.load(f)
	except:
		return 'error'
	return requests.put(URL+'/API/admin/buildings/manage', json=build, auth=('user', 'pass'))

def LoggedUsers():
	i = input('Logged users:\n\t1 - all\n\t2 - by building\n\t\n>> ')
	if i == '1':
		endpoint='/API/admin/users/loggedin'
		r = requests.post(URL+endpoint, auth=('user', 'pass'))
		if r.status_code == 200:
			print('received:',r.json())
			print(">"*20)
			print(*r.json(), sep='\n')
			print("<"*20)
		else:
			print('[{}] Error'.format(r.status_code))
	elif i == '2':
		b = getBuilding()
		s = set()
		for f in b:
			endpoint='/API/admin/buildings/'+f['_id']+'/users'
			r = requests.post(URL+endpoint, auth=('user', 'pass'))
			if r.status_code == 200:
				s = s.union(set(r.json().get('users')))
		print('received:',s)
		print(">"*20)
		print(*s, sep='\n')
		print("<"*20)
	else:
		print('Not a valid option')
		return

def getUsers():
	d = dict()
	resp=requests.post(URL+'/API/admin/users', auth=('user', 'pass'))
	if resp.status_code == 200 and 'application/json' in resp.headers['Content-Type']:
		l = resp.json()
		print('Users:')
		for num , v in enumerate(l,1):
			print('\t{:3} {}'.format(num, v))
		num = input('\nType the number of the user to see their active users [enter to skip]')
		if len(num) ==0:
			return None
		try:
			return [l[int(num)-1]]
		except:
			return None
	else:
		print('[{}] No users available'.format(resp.status_code))
		return None

def getBuilding():
	resp = requests.post(URL+'/API/admin/buildings', auth=('user','pass'))
	if resp.status_code == 200 and 'application/json' in resp.headers['Content-Type']:
		buildings = resp.json()
		d = dict()
		print('Buildings:')
		for num, b in enumerate(buildings,1):
			d[num] = {'_id':b['_id'],'name':b['name'], 'num':num}
			print('\t{:3} {}'.format(num, b['name']))
		num = input('\nType the number of the building to see their active users: ')
		if len(num) == 0:
			return None
		try:
			return [d[int(n)] for n in num.split(',') ]
		except:
			return None
	else:
		print('[{}] No buildings available'.format(resp.status_code))
		return None

def logEntry(e,l, user = None):
	t = e.get('type')
	if t in ('sent','msg','received'):
		if t == 'msg':
			ch = '>>>'
			frm = e.get('info')[0]
			to = e.get('info')[1]
			cnt = e.get('info')[2]

		if t == 'sent':
			ch = '>>>'
			frm = user
			to = ','.join(e.get('info')[0])
			cnt = e.get('info')[1]

		if t == 'received':
			ch = '<<<'
			frm = user
			to = e.get('info')[0]
			cnt = e.get('info')[1]

		f = ' {}{}{} {} {}'.format(color.BOLD,frm,color.END,ch, to)
		return '{}][{} : {}][{}] ════╣{}╠════'.format('msg'.center(len('movement')),l.get('lat'),l.get('lon'),f,cnt)


	if t == 'movement':
		return 'movement][{} : {}]'.format(l.get('lat'),l.get('lon'))



def format(listlogs, user = None):
	return [ "[{}][{}".format(l[0].split(',')[1][1:-4] , logEntry(l[1],l[2], user = user)) for l in listlogs]


def Logs():
	i = input('Logs by:\n\t1 - user\n\t2 - building\n\tother - both\n>> ')
	u = None
	b = None
	try:
		if i != '2':
			u = getUsers()[0]
		if i != '1':
			b = getBuilding()[0]['_id']
	except:
		print("Problems on input")
		return

	if u and b:
		endpoint = '/API/admin/buildings/{}/user/{}/logs'.format(b,u)
	elif u:
		endpoint='/API/admin/users/{}/logs'.format(u)
	elif b:
		endpoint='/API/admin/buildings/{}/logs'.format(b)

	resp = requests.post(URL+endpoint, auth=('user', 'pass'))
	if resp.status_code == 200:
		print('received:',resp.json())
		print(">"*20)
		print(*format(resp.json(),user = u), sep='\n')
		print("<"*20)
	else:
		print('[{}] Error'.format(resp.status_code))

def createBot():
	print('Create bot')
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
				r = requests.put(URL+'/API/admin/bot/create', data = {'buildings':data}, auth=('user', 'pass'))
				if r.status_code == 200 and 'application/json' in resp.headers['Content-Type']:
					print('\nUse the user '+color.BOLD+color.RED+'bot'+color.END+' and pass:',color.BOLD+color.RED+r.json().get('key')+color.END, 'to send message to the building defined')
			except KeyError:
				print("Error on input")
	else:
		print("Error occour")


if __name__ == '__main__':
	while(True):
		print()
		print('''Menu
	1 - setup buildings
	2 - logged in users
	3 - logs
	4 - create bot''')
		try:
			i = int(input('>> '))
			if i == 1:
				file = input('Setup Buildings:\n\tspecify path to file (empty will default buildings.json)>> ')
				if len(file):
					SetBuildings(file=file)
				else:
					SetBuildings()
			elif i == 2:
				LoggedUsers()
			elif i == 3:
				Logs()
			elif i == 4:
				createBot()

		except TypeError:
			pass
		except ValueError:
			pass