class Messages():
	def __init__(self):
		self.received = {'read':[],'new':[]}
		self.send = []

	def Send(self, msg):
		self.send.append(msg)

	def Received(self, type='all'):
		if type == 'all' :
			self.received['read'] += self.received['new']
			return self.received['read']
		
		elif type == 'read' or type=='new':
			return self.received[type]
		
		return None

class User:
	def __init__(self, id : str):
		self.ID = id
		self.Messages = Messages()
		self.Location = {'lat':12, 'lon':14}
		self.Range = 50 #meters
		self.UsersInRange = {}
	

class Management:

	def __init__(self):
		self.Logged = {}
		self.Users = {}

	def Log(u):
		if type(u) == 'str':
			U = self.Users.get(u)
			if U == None:
				U = User(u)
				self.Users[U.ID] = U


		elif type(u) == 'User':
			U = self.Users.get(u.ID)
			if U == None:
				U = User(u)
				self.Users[U.ID] = U
	

		self.Logged[U.ID] = U
