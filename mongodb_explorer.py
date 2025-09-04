from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

def connect_to_mongodb():
    """Connect to MongoDB using the connection string from .env"""
    load_dotenv()
    connection_string = os.getenv('MONGODB_CONNECTION_STRING')
    
    try:
        client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
        # Test connection
        client.server_info()
        return client
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

