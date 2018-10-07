from dbUI import dbUI
import pickle

def main():
	db = pickle.load('backUp')
	if db not None:
		ui = dbUI(db)
	else:
		ui = dbUI()

	try:

	pickle.dump(db, 'bakcUp')

	return 0


if __name__ == "__main__":
	main()
'''
daemon = Pyro4.Daemon()
obj = exposedClass()
uri = daemon.register(obj, "Name")
print("URI:"+uri)
daemon.requestLoop()
'''