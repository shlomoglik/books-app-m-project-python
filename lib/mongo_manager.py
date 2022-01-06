import pymongo


class MongoManager:
     __instance = None
     @staticmethod 
     def getDB(name="libraries-app"):
         if MongoManager.__instance == None:
             MongoManager(name)
         return MongoManager.__instance
     def __init__(self,name):
        if MongoManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoManager.__instance = pymongo.MongoClient('localhost', 27017).get_database(name)