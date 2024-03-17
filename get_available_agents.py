from pymongo import MongoClient
import logging
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

def get_agent_ips_and_names():
    try:
        # Fetch all documents from the 'agents_collection' collection
        agents = agents_collection.find()

        # Extract the IP addresses and agent names
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
