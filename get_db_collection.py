from pymongo import MongoClient
import certifi

def get_db_collection(collection_name: str, db_name: str):
    username = "omnigence_91"
    password = "LakersLebron23" 
    cluster_url = "fqv0kwb.mongodb.net"
    
    # Proper connection string format
    MONGO_URL = f"mongodb+srv://{username}:{password}@{cluster_url}/{db_name}?retryWrites=true&w=majority&authSource=admin"
    #"MDB_MCP_CONNECTION_STRING": "mongodb+srv://omnigence_91:LakersLebron23@omnigence.fqv0kwb.mongodb.net/?retryWrites=true&w=majority&appName=Omnigence"

    try:
        client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())
        # The ping command is cheap and does not require auth.
        print(client.admin.command('ping'))
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

    db = client[db_name]
    
    return client, db[collection_name]