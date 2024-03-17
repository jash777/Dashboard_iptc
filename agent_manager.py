from pymongo import MongoClient
from urllib.parse import quote_plus

class AgentManager:
    def __init__(self):
        # Encode the username and password
        username = "*****"
        password = "*******"
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)

        # Connect to the MongoDB server using the properly escaped username and password
        self.client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@mongodb.server.com")
        
        self.db = self.client['agents_manager']
        self.agents_collections = self.db['agents_collection']

        
        # Collection to store server agent IPs
        self.agents_collection = self.db['agents']

    def get_agents(self):
        return [agent['ip'] for agent in self.agents_collection.find()]

username = "alpha"
password = "Alpha#Jash@777"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@dashboard.wnz5mjp.mongodb.net/")
db = client['agents']
agents_collection = db['agents']
agents_collections = db['agents_collection']
db = client['iptables_db']
rules_collection = db['rules']   