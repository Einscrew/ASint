import Pyro4
from bookDB import bookDB
from os import sys

bookDB_Remote = Pyro4.expose(bookDB)

ns=Pyro4.locateNS()

daemon = Pyro4.core.Daemon(host="localhost")
ns.register("bookDB", daemon.register(bookDB_Remote(), "bookDB"))
daemon.requestLoop()