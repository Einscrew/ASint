import pymongo

class Db():

	def __init__(self, conn="mongodb://localhost:27017/", dbName="asint"):
		self.client = pymongo.MongoClient(conn)
		self.db = self.client[dbName]

	#### Users ####

	def insertUser(self, istID, lat, lon, myRange):
		try:
			self.db["users"].insert_one({"_id": istID, "location":{ "lat": lat, "lon": lon}, "range": myRange})
			return True
		except:
			print("Error inserting user")
			return False

	def removeUser(self, istID):
		try:
			self.db["users"].delete_one({"_id": istID})
			return True
		except:
			print("Error removing user")
			return False

	def updateUserLocation(self, istID, lat, lon):
		try:
			self.db["users"].update_one({"_id": istID}, {"$set": {"lat": lat, "lon": lon}})
			return True
		except:
			print("Error changing user location")
			return False

	def getAllLoggedUsers(self):
		return self.db["users"].find()

	#### Movements ####
	def insertMovement(self, user, location):
		try:
			self.db["movements"].insert_one({"user":user, "location":location })
			return True
		except:
			print("Error inserting movement")
			return False

	def getUserMovements(self, user):
		pass

	#### Messages ####
	def insertMessage(self, src, dest, msg, location):
		try:
			self.db["messages"].insert_one({"src":src, "dst":dst, "content":msg, "location":location })
			return True
		except:
			return False

	def getMessages(self, user):
		try:
			self.db["messages"].find({}, {"dest": 0}) #excludes destiny from the result
			return True
		except:
			return False

	def getAllMessages(self):
		return self.db["messages"].find()

	#### Buildings ####

	#### Bots ####
	def insertBot(self, id):
		try:
			return db["bots"].insert_one({'building':id}).inserted_id.binary
		except:
			print('Error inserting Bot')
			return False

	def deleteBot(self, k):
		try:
			db["bots"].delete_one({'key':k})
			return True
		except:
			return False









