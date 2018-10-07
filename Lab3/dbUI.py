from bookDB import bookDB

class dbUI:
	inputMsg = """
Available commands:
	NEW:[author]:[title]:[year]:[ISBN]
	SHOW:[[ISBN]]
	AUTHORS
	SEARCH_AUTH:[author]
	SEARCH_YEAR:[year]

	>> """
	def __init__(self):
		self.db = bookDB();

	def run(self):
		cmds = {"NEW":self.db.insert,"SHOW":self.db.show,"AUTHORS":self.db.authors,"SEARCH_AUTH":self.db.listBooksBy,"SEARCH_YEAR":self.db.listBooksFrom}
		while(True):
			cmd = input(self.inputMsg).split(':')
			if len(cmd) >= 1:
				print(cmd)
				print("...",*cmd[1:])
				f = cmds[cmd[0].upper()](*cmd[1:])
				print("[reply]:\n",f, sep='')

if __name__ == "__main__":
	ui = dbUI()
	print("Running")
	ui.run()
	