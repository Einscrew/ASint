from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template()

@app.route('/homepage')
def homepage():
	return "homepage"

if __name__ == '__main__':
	app.run()
