from pymongo import MongoClient
import logging
from urllib.parse import quote_plus

username = "alpha"
password = "Alpha#Jash@777"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

client = MongoClient(f"mongodb+srv://{encoded_username}:{encoded_password}@dashboard.wnz5mjp.mongodb.net/") 
db = client['agents']
agents_collection = db['agents_collection']

def get_agent_ips_and_names():
    try:
        agents = agents_collection.find()
        ips = []
        names = []
        for agent in agents:
            ips.append(agent.get('ip_address', ''))
            names.append(agent.get('agent_name', ''))
        print(ips)
        print(names)
        return ips, names
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return [], []

if __name__ == "__main__":
    agent_ips, agent_names = get_agent_ips_and_names()
    print(agent_ips)
    print(agent_names)
