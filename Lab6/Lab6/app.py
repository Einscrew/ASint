from flask import Flask
from flask import render_template
from flask import request
import bookDB

app = Flask(__name__)
db = bookDB.bookDB("mylib")

@app.route('/')
def hello_world():
	count = len(db.listAllBooks())
	return render_template("mainPage.html", count_books=count)

@app.route('/addBooksForm')
def add_Book_Form():
	return render_template("addBookTemplate.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
	if request.method == "GET":
		db.addBook(request.args.get("Author"), request.args.get("Title"), request.args.get("Year"))
		return "You have "+ str(len(db.listAllBooks()))+" books"
	else:
		db.addBook(request.form.get("Author"), request.form.get("Title"), request.form.get("Year"))
		return "You have "+ str(len(db.listAllBooks()))+" books"

@app.route('/showBookForm')
def show_Book_Form():
	return render_template("showBook.html")
	
@app.route('/showBook', methods=['POST', 'GET'])
def show_Book():
	if request.method == "GET":
		book = db.showBook(request.args.get("Id"))
		return  "ola"
	else:
		book = db.showBook(request.form.get("Id"))
		return "ola"

@app.route('/listAllBooks')
def list_All_Books():
	l = db.listAllBooks()
	return render_template("listAllBooks.html", books=[ [b.author, b.title, b.year] for b in l ])


if __name__ == '__main__':
	app.run()
