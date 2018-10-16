from random import randint

class queryDB:
	def __init__(self, db = list()):
		self.dbs = db
	
	def addBook(author, title, year):
		if len(dsb) > 0:
			self.dbs[randint(0, len(dbs))].addBook(author, title, year)
	def showBook(id):
		ret = []
		for i in self.dbs:
			ret.append(i.showBook(id))
		return ret

