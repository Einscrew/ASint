import pymongo

class Db():

	def __init__(self, conn="mongodb://localhost:27017/", dbName="asint"):
		self.client = pymongo.MongoClient(conn)
		self.db = client[dbName]

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





