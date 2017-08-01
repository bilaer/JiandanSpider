import pymongo
import os

class DataManager(object):
    def __init__(self, dbName, collectionName):
        self.InitDB(dbName, collectionName)

    def InitDB(self, dbName, collectionName):
        client = pymongo.MongoClient("localhost", 27017)
        self.db = client[dbName]
        self.collection = self.db[collectionName]


    def saveDataToDB(self, data):
        if isinstance(data, dict):
            postId = self.collection.insert(data)
            return postId
        else:
            print("Error data is not a dict")
            return

    def sortDBbyKey(self, key, range):
        return self.collection.find().sort(key, -1).limit(range)

