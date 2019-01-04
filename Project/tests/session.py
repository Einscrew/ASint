from functools import wraps
from flask import Flask, g, session, redirect, url_for, escape, request
import json
import requests
app = Flask(__name__)

with open("../keys.json",'r') as f:
    APP = json.load(f)


with open("../secret", 'rb') as f:
    app.secret_key = f.read()


APP['redirectURI'] = 'http://127.0.0.1:5000/messages'
APP['loginURI'] = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id='+str(APP['clientID'])+'&redirect_uri='+APP['redirectURI']

# Set the secret key to some random bytes. Keep this really secret!


def getUserInfo():
    access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
    request_data = {'client_id': int(APP['clientID']), 'client_secret': APP['clientSecret'],
            'redirect_uri': APP['redirectURI'], 'code': session['code'], 'grant_type': 'authorization_code'}

    reqAccessToken = requests.post(access_token_request_url, data=request_data)

    '''
    if reqAccessToken. ok:
        del(session['code'])
    '''

    session['access_token'] = reqAccessToken.json().get('access_token')
    session['refresh_token'] = reqAccessToken.json().get('refresh_token')
    session['token_expires'] =  reqAccessToken.json().get('expires_in')

    params = {'access_token': session['access_token']}
    request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)
    session['username'] = request_info.json().get('username')
    return session['username']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if 'username' not in session or c is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/secret')
@login_required
def secret():
    return 'secret, shhhhhh.......'

@app.route('/messages')
def messages():

    session['code'] = request.args.get('code')
    
    if session['code'] is None and 'username' not in session:
        return redirect(APP['loginURI'])

    elif session['code'] is not None and 'username' not in session:
        getUserInfo()
        return redirect(url_for('messages'))

        
    return 'logged in ' + session['username']
'''
    if 'code' in session and 'access_token' not in session:

        getUserInfo()

        return redirect(url_for('messages'))

        ##render template(main)
    
    if c is None and 'username' not in session:
        return redirect(APP['loginURI'])
    else:
        session['code'] = c
        return redirect(url_for('messages'))
    
    ##if 'access_token' in session:        
    #transfers = requests.get('https://transfer.api.globusonline.org/v0.10/task_list?limit=1',headers={'Authorization': 'Bearer ' + session['access_token']})
'''
@app.route

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(request.next or url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
