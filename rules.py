import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["iptables_rules"]
collection = db["rules"]
inbound_rules_collection = db['inbound_rules']
outbound_rules_collection = db['outbound_rules']

# Fetch predefined rules from MongoDB
predefined_rules = collection.find()
# Convert MongoDB cursor to list of dictionaries
predefined_rules_list = list(predefined_rules)
# Now, `predefined_rules_list` contains the fetched predefined rules
# You can pass this list to your Flask route for rendering the template
