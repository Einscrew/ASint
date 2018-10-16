#!/usr/bin/env python

import Pyro4
import bookDB
import random



Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

def main():
        remoteLibrary = Pyro4.expose(bookDB.bookDB)

        db = bookDB.bookDB("mylib")


        daemon = Pyro4.Daemon(host='194.210.229.157')
        print(daemon)
        ns = Pyro4.locateNS(host='193.136.128.104', port=9090)
        print (ns)

        try:
                ns.createGroup(':libraries')
        except:
                pass

        uri = daemon.register(db, "bookDB-Einstein")
        ns.register("bookDB-Einstein-{}".format(random.randint(0,5)), uri)

        try:
                daemon.requestLoop()
        finally:
                daemon.shutdown(True)

if __name__=="__main__":
        main() 
