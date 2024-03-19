from pymongo import MongoClient
from urllib.parse import quote_plus

class AgentManager:
    def __init__(self):
        #username and password
        username = "alpha"
        password = "Alpha#Jash@777"
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)

        #  MongoDB server 
        self.client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@dashboard.wnz5mjp.mongodb.net/")
        
        self.db = self.client['agents_manager']
        self.agents_collections = self.db['agents_collection']

        
        #  store server agent 
        self.agents_collection = self.db['agents']

    def get_agents(self):
        return [agent['ip'] for agent in self.agents_collection.find()]

username = "********"
password = "************"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@mongodb.server.com")
db = client['agents']
agents_collection = db['agents']
agents_collections = db['agents_collection']
db = client['iptables_db']
<<<<<<< HEAD
rules_collection = db['rules']  
=======
rules_collection = db['rules']   
>>>>>>> 65eb53d13db42ddab6aa8b6fe50798ce1312932e
