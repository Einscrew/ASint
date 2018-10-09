from book import book

class bookDB:
	def __init__(self):
		self.books = list()

	def insert(self, *d):
		if len(d) == 1 and isinstance(d[0], book):
			self.books.append(d)
			return "book inserted"
		elif len(d) == 4 and all(isinstance(x, str) for x in d):
			b = book(*d)
			if b != None:
				self.books.append(b)
				return "book inserted"
		return "book NOT inserted"

	def show(self, isbn):
		for i in self.books:
			if i.ISBN == isbn:
				return i.title + ' by ' + i.author + ', '+i.pub_year+' '+i.ISBN + '\n'
		return None

	def show(self):
		s = ''
		for i in self.books:
			s += i.title + ' by ' + i.author + ', '+i.pub_year+' '+i.ISBN + '\n'
		return s

	def authors(self):
		for i in self.books:
				return i.author + '\n'
		return None

	def listBooksBy(self, author):
		for i in self.books:
			if i.author == author:
				return i.title + ' by ' + i.author + ', '+i.pub_year+' '+i.ISBN + '\n'
		return None

	def listBooksFrom(self, year):
		for i in self.books:
			if i.pub_year == year:
				return i.title + ' by ' + i.author + ', '+i.pub_year+' '+i.ISBN + '\n'
		return None


if __name__ == "__main__":
	db = bookDB()
	db.insert(book("Saramago", "A viagem do elefante", "1998", "ISNB-123D-3SN9-N1U9"))
	db.insert(book("Orwell", "Animal farm", "1965", "ISNB-1G0B-J38H-N81D"))
	print(db.show())
	print(db.listBooksFrom("Saramago"))
