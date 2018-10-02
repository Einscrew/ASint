import socket
from sys import exit
from Int import Integer
import pickle

s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host, port))
print(s.recv(1024).decode('utf-8'))

while True:
	s.send( str(input("insert int:")).encode('utf-8'))
	#pickle.load(i, s.fileno())
	i = pickle.loads(s.recv(1024))
	print(i.Value())
