import Pyro4

nameserver=Pyro4.locateNS()
obj = Pyro4.Proxy(nameserver.lookup("bookDB"))

obj.insert("Saramgo", "Viagem do Elefante", "1990", "ISBN-12DF-62AJ")
print(obj.show())