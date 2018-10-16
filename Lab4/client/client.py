#!/usr/bin/env python

import Pyro4
import dbUI


Pyro4.config.SERIALIZER = 'pickle'

def main():
        ns = Pyro4.locateNS(host='193.136.128.104', port=9090)
        uri = ns.list('bookDB-Einstein')
        
        print(uri)
        db = list()
        for uri in uri.values():
        	db.append(Pyro4.Proxy(uri))

        
        ui = dbUI.dbUI(db)
        ui.menu()

if __name__=="__main__":
        main() 
