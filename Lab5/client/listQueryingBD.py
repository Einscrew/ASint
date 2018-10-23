from random import randint

class queryDB:
	def __init__(self, db):
		self.dbs = db
	
	def addBook(self, author, title, year):
		if len(self.dbs) > 0:
			self.dbs[randint(0, len(self.dbs)-1)].addBook(author, title, year)
	def showBook(self, id):
		ret = []
		for i in self.dbs:
			ret.append(i.showBook(id))
		return ret

	def listAllBooks(self):
		books = []
		for db in self.dbs:
			books.append(db.listAllBooks())
		return books

	def listBooksAuthor(self, authorName):
		authors = []
		for b in self.dbs:
			authors.append(b.listBooksAuthor(authorName))
		return authors
	def listBooksYear(self, year):
		books = []
		for b in self.dbs:
			books.append(b.listBooksYear(year))
		return books




