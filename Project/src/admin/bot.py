#!/usr/bin/env python3
import requests
import json
#URL = 'https://asint-2018.appspot.com'
URL = 'http://127.0.0.1:5000'


if __name__ == '__main__':
	k = input('insert your bot key: ')

	while True:
		r = requests.post(URL+'/API/bots/'+k+'/message', data = input('Insert the content to be send: '), auth=('bot',k))
		if r.status_code == 200:
			print('[',r.status_code,']',r.content)
		else:
			print('[',r.status_code,']','Error')