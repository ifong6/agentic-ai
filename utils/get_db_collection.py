import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
# Create Mongo client

def get_db_collection(collection_name: str, db_name: str):
    client = MongoClient(os.getenv("MONGO_URL"))
    db = client[db_name]
    
    return client, db[collection_name]