import socket
from sys import exit 
s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host, port))
print(s.recv(1024).decode('utf-8'))

while True:
	st = input("Requests:\n\tPush\n\tPop\n\tAdd\n>");
	if st == "Push":
		print( st +" send code:",s.send( (st+" "+input("insert int:")).encode('utf-8') ))
	elif st=="Pop":
		print( st +" send code:",s.send(st.encode('utf-8')))
	elif st=="Add":
		print( st +" send code:",s.send(st.encode('utf-8')))
	else:
		print("closing")
		s.close()
		exit(0)
	
	print(s.recv(1024).decode('utf-8'))
