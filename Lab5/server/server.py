#!/usr/bin/env python

import Pyro4
import bookDB
import random



Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

def main():
        remoteLibrary = Pyro4.expose(bookDB.bookDB)

        db = bookDB.bookDB("mylib")


        daemon = Pyro4.Daemon(host='194.210.229.232')
        print(daemon)
        ns = Pyro4.locateNS(host='193.136.128.108', port=9090)
        print (ns)

        try:
                ns.createGroup(':libraries')
        except:
                pass

        uri = daemon.register(db, "BookDB-81074-81731")
        ns.register("BookDB-81074-81731-{}".format(random.randint(0,5)), uri)

        try:
                daemon.requestLoop()
        finally:
                daemon.shutdown(True)

if __name__=="__main__":
        main() 
