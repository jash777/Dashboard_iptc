from pymongo import MongoClient

class AgentManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['agents_manager']  # Replace 'your_database_name' with your actual database name
        self.agents_collection = self.db['agents']  # Collection to store server agent IPs


    def get_agents(self):
        return [agent['ip'] for agent in self.agents_collection.find()]
