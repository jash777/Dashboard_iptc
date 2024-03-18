import pymongo

# MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["iptables_rules"]
collection = db["rules"]
inbound_rules_collection = db['inbound_rules']
outbound_rules_collection = db['outbound_rules']
predefined_rules = collection.find()
predefined_rules_list = list(predefined_rules)
