import socket
from rpn import rpnCalculator

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
			if st.split()[0] == "Push":
				print("< valid PUsh")
				rpn.push(int(st.split()[1]))
				rpn.print();
				c.send('Push done'.encode('utf-8'))
			elif st=="Pop":
				c.send(str(rpn.pop()).encode('utf-8'))
			elif st=="Add":
				c.send(str(rpn.add()).encode('utf-8'))
			else:
				c.close()
				break
		else:
			c.close()
			break
		
