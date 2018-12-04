import pymongo
from datetime import datetime

class Db():

	def __init__(self, conn="mongodb://localhost:27017/", dbName="asint"):
		self.client = pymongo.MongoClient(conn)
		self.db = self.client[dbName]

	#### Users ####

	def insertUser(self, istID, location, myRange):
		try:
			self.db["users"].insert_one({"_id": istID, "location": location, "range": myRange})
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
			self.db["users"].update_one({"_id": istID}, {"$set": {"location": location}})
			return True
		except:
			print("Error changing user location")
			return False

	def updateUserRange(self, newRange):
		try:
			self.db["users"].update_one({"_id": istID}, {"$set": {"range": myRange}})
			return True
		except:
			print("Error changing user range")
			return False

	def getAllLoggedUsers(self):
		return self.db["users"].find()

	#### Movements ####
	def insertMovement(self, user, location, buildingID):
		try:
			self.db["movements"].insert_one({"user":user, "location":location, "building": buildingID, "time": datetime.now()})
			return True
		except:
			print("Error inserting movement")
			return False

	def getUserMovements(self, user):
		return self.db["movements"].find({"_id": user})

	def getBuildingMovements(self, buildingID):
		return self.db["movements"].find({"building": buildingID}).sort("time", pymongo.ASCENDING)

	#### Messages ####
	def insertMessage(self, src, dest, msg, location, buildingID):
		try:
			self.db["messages"].insert_one({"src": src, "dst": dst, "content": msg, "location": location, "building": buildingID ,"time": datetime.now()})
			return True
		except:
			print("Error inserting message")
			return False

	def getUserMessages(self, user):
		try:
			self.db["messages"].find({}, {"dest": 0}) #excludes destiny from the result
			return True
		except:
			print("Error getting messages")
			return False

	def getAllMessages(self):
		return self.db["messages"].find()

	def getBuildingMessages(self, buildingID):
		return self.db["messages"].find({"building": buildingID}).sort("time", pymongo.ASCENDING)

	#### Buildings ####
	def insertBuildings(self, buildingsList):
		try:
			self.db["buildings"].insert_many(buildingsList)
			return True
		except:
			print("Error inserting movement")
			return False

	#### Bots ####







