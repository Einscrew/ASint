import pymongo
from datetime import datetime
import geo

class Db():

	def __init__(self, conn='mongodb://localhost:27017/', dbName='asint'):
		self.client = pymongo.MongoClient(conn)
		self.db = self.client[dbName]
	
	#________________________________________________________________________
	#### Users ####
	def insertUser(self, istID, location, myRange):
		try:
			self.db['users'].insert_one({'_id': istID, 'location': location, 'range': myRange, 'building': None})
			return True
		except:
			print('Error inserting user')
			return False

	def removeUser(self, istID):
		try:
			self.db['users'].delete_one({'_id': istID})
			return True
		except:
			print('Error removing user')
			return False

	def updateUserLocation(self, istID, location):
		try:
			self.db['users'].update_one({'_id': istID}, {'$set': {'location': location}})
			return True
		except:
			print('Error changing user location')
			return False

	def updateUserRange(self, istID, newRange):
		try:
			self.db['users'].update_one({'_id': istID}, {'$set': {'range': newRange}})
			return True
		except:
			print('Error updating user range')
			return False

	# Returns the building where user is and None if the user is outside of buildings
	def getUserBuilding(self, istID):
		user = self.db['users'].find_one({'_id': istID})
		allBuildings = self.db['buildings'].find()
		inBuilding= lambda u1,u2: geo.distance(u1['location'],u2['location']) < 50
		for building in allBuildings:
			if inBuilding(user, building):
				self.db['users'].update_one({'_id': istID}, {'$set': {'building': building['_id']}}) 
				return True
		return False


	def getAllLoggedUsers(self):
		return self.db['users'].find()

	def getUsersInRange(self, istID):
		u = self.db['users'].find_one({'_id':istID})
		print(u)

		inRange = lambda u1,u2: geo.distance(u1['location'],u2['location']) < u1['range']

		allusers = self.db['users'].find()

		return [user['_id'] for user in allusers if user['_id'] != istID and inRange(u,user)]

	# TO DO
	def getUsersInSameBuilding(self, istID):
		user = self.db['users'].find_one({'_id': istID})

		if user['building'] != None:
			return None
		else:
			return None

	#________________________________________________________________________
	#### Movements ####
	def insertMovement(self, user, location, buildingID):
		try:
			self.db['movements'].insert_one({'user':user, 'location':location, 'building': buildingID, 'time': datetime.now()})
			return True
		except:
			print('Error inserting movement')
			return False

	def getUserMovements(self, user):
		return self.db['movements'].find({'_id': user})

	def getBuildingMovements(self, buildingID):
		return self.db['movements'].find({'building': buildingID})

	#________________________________________________________________________
	#### Messages ####
	def insertMessage(self, src, dest, msg, location, buildingID):
		try:
			self.db['messages'].insert_one({'src': src, 'dst': dest, 'content': msg, 'location': location, 'building': buildingID ,'time': datetime.now()})
			return True
		except:
			print('Error inserting message')
			return False

	def getUserMessages(self, user):	
		try:
			r = [ [i['src'],i['content']] for i in self.db['messages'].find({'dst': user})]
			print(r)
			return r#excludes destiny from the result
		except:
			print('Error getting messages')
			return False

	def getAllMessages(self):
		return [i['content'] for i in self.db['messages'].find()]

	def getBuildingMessages(self, buildingID):
		return self.db['messages'].find({'building': buildingID})
	#________________________________________________________________________
	#### Buildings ####
	def insertBuildings(self, buildingsList):
		try:
			#self.db["buildings"].drop()
			self.db["buildings"].insert_many(buildingsList)
			return True
		except:
			print('Error inserting movement')
			return False

	def getBuildings(self):
		s = self.db["buildings"].find({},{'_id':0})
		return list(s)

	#________________________________________________________________________
	#### Bots ####
	def insertBot(self, id):
		try:
			return db['bots'].insert_one({'building':id}).inserted_id.binary
		except:
			print('Error inserting Bot')
			return False

	def deleteBot(self, k):
		try:
			db['bots'].delete_one({'key':k})
			return True
		except:
			return False

		




