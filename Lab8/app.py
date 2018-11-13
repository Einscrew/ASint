from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
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
	id = -1
	if request.method == "GET":
		id = int(request.args.get("Id"))
	else:
		id = int(request.form.get("Id"))

	book = db.showBook(id)
	return render_template("renderBook.html", books = book.__list__)

@app.route('/listAllBooks')
def list_All_Books():
	l = db.listAllBooks()
	return render_template("listAllBooks.html", books=[ [b.author, b.title, b.year, b.likes, b.id] for b in l ])

@app.route('/API/Books', methods=['POST'])
def API_list_books():
	l = db.listAllBooks()
	jlist =  [ i.__dict__ for i in l ]
	return jsonify(jlist)

@app.route('/API/Books/<int:id>/', methods=['POST'])
def API_list_book(id):
	l = db.showBook(id)
	return jsonify(l.__dict__)

@app.route('/API/Books/<int:id>/like', methods=['POST', 'GET'])
def API_list_book_likes(id):
	if request.method == "GET":
		b = db.showBook(id)
		return "<p> likes: " + str(b.likes)+"</p>"
	else:
		l = db.likeBook(id)
		return jsonify({"likes":l})


if __name__ == '__main__':
	app.run()
