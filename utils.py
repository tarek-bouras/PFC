from pymongo import MongoClient
 
def get_db_handle():
    client = MongoClient("mongodb://localhost:27017/")
    db_handle = client['DataLake']
    return db_handle

def get_collection_handle(db_handle,data):
    return db_handle[data]