from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads

class StoreMongoDB(object):
    def __init__(self, clientaddr_port = "localhost:27017"):
        self.client = MongoClient(clientaddr_port)
    
    #DB Instanz erstellen oder aufrufen
    def create_opendb(self, dbinstance = "Acceleration"):
        self.db_acc = self.client[dbinstance]
        print(f"DB instance ({dbinstance}) created!")
    
    #Daten in die DB packen
    def getindb(self, data):
        #Packt jedes Element rein als Dictionary
        array = [{'ax': data[0], 'ay': data[1], 'az': data[2]}]

        self.db_acc.Accelerations.insert_many(array)