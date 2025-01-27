from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configManager import configManager

class mongoCollector:
    def __init__(self):
        self.uri=configManager().MONGO_URI
        self.client=MongoClient(self.uri, server_api=ServerApi('1'))
        assert self.ping_check(), "MongoDB connection failed"
        self.collection=self.create_collection()



    def ping_check(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            print("Initiating your request")
            return True
        except Exception as e:
            print(e)
            return False
    
    def create_collection(self,db="RAG",collection="rag"):
        db = self.client[db]
        collection = db[collection]
        return collection
    
    def insert_data(self,id,data):
        assert len(id) > 0, "Id cannot be empty"
        assert len(data) > 0, "Data cannot be empty"
        assert len(data) == len(id), "Id and data should have same length"

        for i in range(len(id)):
                try:
                    self.collection.insert_one({"_id":id[i],"text":data[i]})
                except Exception as e:
                    print(e)
        print("Data inserted into MongoDB successfully")

    def get_data(self,id):
        texts=[]
        assert len(id) > 0, "Id cannot be empty"
        for i in range(len(id)):
            try:
                 texts.append(self.collection.find_one({"_id":id[i]})['text'])
            except Exception as e:
                print(e)
        return texts

            


if __name__=="__main__":
    collector=mongoCollector()
    collector.insert_data([4],["Abhishek Singh Rathore"])
    print(collector.collection.find_one({"_id":4})['text'])
    print(type(collector.collection.find_one({"_id":4})))



        
    




