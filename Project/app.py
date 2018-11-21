from flask import Flask
import fenixedu

app = Flask(__name__)

@app.route('/')
def hello_world():
	config = fenixedu.FenixEduConfiguration('570015174623316', '/homepage', 'azBWoZcEZJhSVHM+QVrtyzOvMl3UK0T+XtJzBuxmAI8DeQ+eW2Ps0DOS9bloB91j4KSECpSSeikePNcIhGEwwA==', '127.0.0.1:5000/')
	client = fenixedu.FenixEduClient(config)
	return client.get_spaces()

@app.route('/homepage')
def homepage():
	return "homepage"

if __name__ == '__main__':
	app.run()
