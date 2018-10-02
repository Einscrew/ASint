import socket
from rpn import rpnCalculator
from Int import Integer
import pickle

rpn = rpnCalculator()
s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)

while True:
	c, addr = s.accept()
	print('Connection from', addr)

	c.send('Hello'.encode('utf-8'))
	while True:
		st = c.recv(1024).decode('utf-8')
		if(len(st) > 0):
			#pickle.dump(Integer(int(st)), c.fileno())
			c.send(pickle.dumps(Integer(int(st))))
		else:
			c.close()
			break
		
