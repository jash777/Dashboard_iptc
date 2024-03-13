from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, emit
from rules import *
from agent_manager import AgentManager
from get_available_agents import get_agent_ips_and_names
import requests
import logging
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)
app.secret_key = b'ESANHKD8976DS8DSA$^*&^*&BOH9YWSDF#'
socketio = SocketIO(app)

client = MongoClient('mongodb://localhost:27017/') 
db = client['agents']
agents_collection = db['agents']
db = client['iptables_db']
rules_collection = db['rules']

logging.basicConfig(filename='All_log.log', level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        agent_ips, agent_names = get_agent_ips_and_names()  # This function should return agent IPs and names
        agent_options = ['{} - {}'.format(ip, name) for ip, name in zip(agent_ips, agent_names)]
        return render_template('index.html', agent_options=agent_options, predefined_rules=predefined_rules_list)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        return "An error occurred while loading the page."
    
# @app.route('/select_agent', methods=['POST'])
# def select_agent():
#     try:
#         selected_value = request.form.get('agent_ip')
#         selected_ip = selected_value.split(' - ')[0] if selected_value else None

#         if selected_ip:
#             session['AGENT_URL'] = f'http://{selected_ip}:5000'
#             logger.info("Selected agent is %s", session['AGENT_URL'])

#             # Save agent info to MongoDB
#             agent_data = {'ip': selected_ip, 'name': selected_value.split(' - ')[1]}
#             agents_collection.insert_one(agent_data)

#             return redirect(url_for('index'))
#         else:
#             return "Invalid selection of agent."
#     except Exception as e:
#         logger.error("An error occurred while selecting agent: %s", str(e))
#         return "An error occurred while selecting agent."

@app.route('/select_agent', methods=['POST'])
def select_agent():
    try:
        selected_value = request.form.get('agent_ip')
        selected_ip = selected_value.split(' - ')[0] if selected_value else None

        if selected_ip:
            session['AGENT_URL'] = f'http://{selected_ip}:5000'
            logger.info("Selected agent is %s", session['AGENT_URL'])

            # Save agent info to MongoDB
            agent_data = {'ip': selected_ip, 'name': selected_value.split(' - ')[1]}
            agents_collection.insert_one(agent_data)

            return redirect(url_for('index'))
        else:
            return "Invalid selection of agent."
    except Exception as e:
        logger.error("An error occurred while selecting agent: %s", str(e))
        return "An error occurred while selecting agent."


@app.route('/inbound-rules', methods=['POST'])
def apply_inbound_rule():
    try:
        inbound_rule = request.json.get('inbound_rule')
        logger.info("Received inbound rule data: %s", inbound_rule)  # Log the received data
        
        if inbound_rule:
            # Log the content of the request being sent to AGENT_URL
            logger.info("Sending request to AGENT_URL: %s", session.get("AGENT_URL"))
            logger.info("Request payload: %s", request.json)
            
            response = requests.post(f'{session.get("AGENT_URL")}/inbound_rule', json={'inbound_rule': inbound_rule})
            # Log the response content or status code
            if response.status_code == 200:
                logging.info("Response from agent: %s", response.json())
            else:
                logging.error("Error response from agent: %s", response.status_code)
            
            # Return appropriate response to the client
            if response.status_code == 200:
                return jsonify({'message': 'Inbound rule applied successfully to the agent'}), 200
            else:
                return jsonify({'error': 'Error applying inbound rule to the agent'}), 500
        else:
            return jsonify({'error': 'No inbound rule provided'}), 400
    except requests.RequestException as e:
        logger.error("Error occurred while sending request to agent server: %s", str(e))
        return jsonify({'error': 'Error sending request to the agent server'}), 500
    except Exception as e:
        logger.error("An unexpected error occurred while applying inbound rule: %s", str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/outbound-rules', methods=['POST'])
def apply_outbound_rule():
    try:
        outbound_rule = request.json.get('outbound_rule')
        logger.info("Received inbound rule data: %s", outbound_rule)  # Log the received data
        
        if outbound_rule:
            # Log the content of the request being sent to AGENT_URL
            logger.info("Sending request to AGENT_URL: %s", session.get("AGENT_URL"))
            logger.info("Request payload: %s", request.json)
            
            response = requests.post(f'{session.get("AGENT_URL")}/outbound_rule', json={'outbound_rule': outbound_rule})
            # Log the response content or status code
            if response.status_code == 200:
                logging.info("Response from agent: %s", response.json())
            else:
                logging.error("Error response from agent: %s", response.status_code)
            
            # Return appropriate response to the client
            if response.status_code == 200:
                return jsonify({'message': 'Inbound rule applied successfully to the agent'}), 200
            else:
                return jsonify({'error': 'Error applying inbound rule to the agent'}), 500
        else:
            return jsonify({'error': 'No inbound rule provided'}), 400
    except requests.RequestException as e:
        logger.error("Error occurred while sending request to agent server: %s", str(e))
        return jsonify({'error': 'Error sending request to the agent server'}), 500
    except Exception as e:
        logger.error("An unexpected error occurred while applying inbound rule: %s", str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5070)
