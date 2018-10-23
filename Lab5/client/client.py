#!/usr/bin/env python

import Pyro4
import dbUI
from listQueryingBD import queryDB

Pyro4.config.SERIALIZER = 'pickle'

def main():
    ns = Pyro4.locateNS(host='193.136.128.108', port=9090)
    #uri = ns.list('bookDB-Einstein')
    uri = ns.list('BookDB-81074-81731')
    
    print(uri)
    db = list()
    for uri in uri.values():
    	db.append(Pyro4.Proxy(uri))

    ui = dbUI.dbUI(queryDB(db))
    ui.menu()

if __name__=="__main__":
    main() 
