#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template("mainPage.html")

@app.route('/login')
def homepage():
	return "<a href='/messages'>Login</a>"

@app.route('/messages')
def messages():
	return render_template("messages.html")

if __name__ == '__main__':
	app.run()
