import pymongo
from pymongo import MongoClient

# MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")

from urllib.parse import quote_plus

username = "alpha"
password = "Alpha#Jash@777"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@dashboard.wnz5mjp.mongodb.net/") 


db = client["iptables_rules"]
collection = db["rules"]
inbound_rules_collection = db['inbound_rules']
outbound_rules_collection = db['outbound_rules']
predefined_rules = collection.find()
predefined_rules_list = list(predefined_rules)
