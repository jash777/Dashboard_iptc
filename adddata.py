from pymongo import MongoClient
from urllib.parse import quote_plus

# Encode the username and password
username = "alpha"
password = "Alpha#Jash@777"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Connect to the MongoDB server using the properly escaped username and password
client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@dashboard.wnz5mjp.mongodb.net/") 

# Replace 'agents' with your actual database name
db = client['agents']
agents_collection = db['agents_collection']

# Data to be inserted
data = {
    "agent_id": "12",
    "agent_name": "home server",
    "status": "live",
    "ip_address": "192.168.1.25"
}

# Insert data into the collection
result = agents_collection.insert_one(data)

# Print the inserted document ID
print("Inserted document ID:", result.inserted_id)
