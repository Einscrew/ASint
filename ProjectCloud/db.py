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
	def getUsers(self):
		return [l['_id'] for l in self.db['users'].find()]

	def insertUser(self, istID, location, myRange):
		try:
			self.db['users'].insert_one({'_id': istID, 'location': location, 'range': myRange, 'building': None})#update_one({'_id': istID}, {'_id': istID, 'location': location, 'range': myRange, 'building': None},upsert=True)
			return myRange
		except pymongo.errors.DuplicateKeyError:
			print('Error inserting user, because already exists')
			return self.db['users'].find_one({'_id': istID}).get('range')

	def removeUser(self, istID):
		try:
			self.db['users'].delete_one({'_id': istID})
			return True
		except:
			print('Error removing user')
			return False

	def updateUserLocation(self, istID, location):
		print('user update')
		self.db['users'].update_one({'_id': istID}, {'$set': {'location': location}})
		print('location done')
		self.insertMovement(istID, location, self.getUserBuilding(istID))
		print('inserting Movements')
		try:			
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
		inBuilding= lambda u1,u2: geo.distance(u1['location'],u2['location']) < 20

		buildings = [b['_id'] for b in allBuildings if inBuilding(user, b)]

		self.db['users'].update_one({'_id': istID}, {'$set': {'building': buildings}})

		return buildings

	def getUsersInRange(self, istID, allusers):
		u = self.db['users'].find_one({'_id':istID})
		inRange = lambda u1,u2: geo.distance(u1['location'],u2['location']) < u1['range']

		users = self.db['users'].find({'_id':{'$in':allusers}})

		return set(user['_id'] for user in users if user['_id'] != istID and inRange(u,user))

	def getUsersInSameBuilding(self, filter, allusers):
		istID = filter.get('istID')
		if istID:
			user = self.db['users'].find_one({'_id': istID})
			building = user['building']

		else:
			building = filter.get('building')

		users = self.db['users'].find({'_id':{'$in':allusers}})
		if building != None:
			return set(u['_id'] for u in users if u['_id'] != istID and not set(u['building']).isdisjoint(building))
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
		return self.db['movements'].find({'user': user}).sort('time')

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

	def insertMessage(self, src, dest, msg):
		try:
			u = self.db['users'].find_one({'_id':src})
			self.db['messages'].insert_one({'src': src, 
											'dst': dest,
											'content': msg, 
											'location': u['location'], 
											'building': u['building'],
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

	def getUserSentMessages(self, user, lastIndex=0):
		try:
			r = [ [i['dst'],i['content'], i['time']] for i in self.db['messages'].find({'src': user}).skip(lastIndex)]#.sort(key=lambda e: e[2])
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

		




