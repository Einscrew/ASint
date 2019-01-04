from functools import wraps
from flask import Flask, g, session, redirect, url_for, escape, request, render_template
import datetime
import json
import requests

app = Flask(__name__)
with open("../secret", 'rb') as f:
    app.secret_key = f.read()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session['username'], kwargs)
        if 'username' not in session:#c is None:
            return redirect(url_for('login', next=request.url))
        if session['username'] not in kwargs.values():
            return 'You are banned'
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    print("before callllldddd")
    if 'username' in session and request.endpoint == 'message': 
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=1)
        session.modified = True

@app.route('/')
def index():
    if 'username' in session:
        return render_template('testeSavefy.html',istID=session['username'])#'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/secret/<string:u>', methods=['POST'])
@login_required
def secret(u):
    return 'secret, shhhhhh....... this is from '+u+' you are : '+session['username']

@app.route('/message')
def message():
    print('POSTED')
    return 'POSTED'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
        #return redirect(request.next or url_for('index'))
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
