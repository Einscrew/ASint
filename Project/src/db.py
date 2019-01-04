import pymongo
from bson import ObjectId
from datetime import datetime
import geo

connString = 'mongodb://asint:#asint2018@saint-shard-00-00-xygyu.gcp.mongodb.net:27017,saint-shard-00-01-xygyu.gcp.mongodb.net:27017,saint-shard-00-02-xygyu.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Saint-shard-0&authSource=admin&retryWrites=true'

class Db():

	def __init__(self, conn=connString, dbName='asint'):
		self.client = pymongo.MongoClient(conn)
		self.db = self.client[dbName]
		self.bots = self.db['bots']
	
	#________________________________________________________________________
	#### Users ####
	def insertUser(self, istID, location, myRange):
		try:
			self.db['users'].insert_one({'_id': istID, 'location': location, 'range': myRange, 'building': None})#update_one({'_id': istID}, {'_id': istID, 'location': location, 'range': myRange, 'building': None},upsert=True)
			return True
		except pymongo.errors.DuplicateKeyError:
			print('Error inserting user, because already exists')
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
		inRange = lambda u1,u2: geo.distance(u1['location'],u2['location']) < u1['range']

		allusers = self.db['users'].find()

		return set(user['_id'] for user in allusers if user['_id'] != istID and inRange(u,user))

	def getUsersInSameBuilding(self, istID):
		user = self.db['users'].find_one({'_id': istID})
		allusers = self.db['users'].find()

		if user['building'] != None:
			return set(u['_id'] for u in allusers if u['_id'] != istID and u['building'] == user['building'])
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
		return self.db['movements'].find({'_id': user}).sort('time')

	def getBuildingMovements(self, buildingID):
		return self.db['movements'].find({'building': buildingID}).sort('time')

	#________________________________________________________________________
	#### Messages ####
	def insertMessageInBuilding(self, src, msg, buildingID):
		dest = self.db['users'].find({'building': {'$eq':buildingID}})
		r = dest.count()
		if r > 0:
			s = self.getBuildings(id = buildingID)
			if len(s) == 1:
				self.insertMessage({'src': src,
									'dst': [ d['_id'] for d in dest ], 
									'content': msg, 
									'location': s[0]['location'], 
									'building': buildingID ,
									'time': datetime.now()})
		return r

	def insertMessage(self, src, dest, msg, location, buildingID):
		try:
			self.db['messages'].insert_one({'src': src, 
											'dst': dest,
											'content': msg, 
											'location': location, 
											'building': buildingID,
											'time': datetime.now()})
			return True
		except:
			print('Error inserting message')
			return False

	def getUserMessages(self, user, lastIndex=0):
		lastIndex = lastIndex if lastIndex > 0 else 0
		try:
			r = [ [i['src'],i['content'], i['time']] for i in self.db['messages'].find({'dst': user}).skip(lastIndex)]#.sort(key=lambda e: e[2])
			return r#excludes destiny from the result
		except:
			print('Error getting messages')
			return False

	def getAllMessages(self):
		return [i['content'] for i in self.db['messages'].find()]

	def getBuildingMessages(self, buildingID):
		return self.db['messages'].find({'building': buildingID}).sort('time')
	#________________________________________________________________________
	#### Buildings ####
	def insertBuildings(self, buildingsList):
		try:
			self.removeBuildings()
			self.db["buildings"].insert_many(buildingsList)
			return True
		except:
			print('Error inserting movement')
			return False

	def getBuildings(self, id = None):
		if id is not None:
			s = self.db["buildings"].find({'_id':{'$eq':id}})
		else:
			s = self.db["buildings"].find()
		return list(s)

	def removeBuildings(self):
		self.db["buildings"].drop()

	#________________________________________________________________________
	#### Bots ####
	def insertBot(self, ids):
		try:
			return self.db['bots'].insert_one({'building':ids}).inserted_id.binary.hex()
		except:
			print('Error inserting Bot')
			return False

	def getBot(self, id):	
		try:
			i = self.db['bots'].find({'_id':ObjectId(id)})
			if i.count() != 0:
				return i.next()['building']
			else:
				return None
		except:
			print("Error searching for bot",id)
			return None


	def deleteBot(self, k):
		try:
			self.db['bots'].delete_one({'key':k})
			return True
		except:
			return False

		




