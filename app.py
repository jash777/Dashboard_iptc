from flask import Flask, render_template, request, jsonify, redirect, url_for, session,send_file,make_response
from flask_socketio import SocketIO, emit
from rules import *
from agent_manager import *
from get_available_agents import get_agent_ips_and_names
import requests
import logging
from pymongo import MongoClient
from bson import ObjectId
import json
import os
from urllib.parse import quote_plus
from functools import wraps
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = b'ESANHKD8976DS8DSA$^*&^*&BOH9YWSDF#'
socketio = SocketIO(app)

logging.basicConfig(filename='All_log.log', level=logging.INFO)
logger = logging.getLogger(__name__)
AUTH_KEY = os.getenv("AUTH_KEY")

# Update the index route to include authentication check
@app.route('/')
def index():
    try:
        # Check if user is authenticated
        if 'authenticated' not in session:
            return redirect(url_for('login'))  # Redirect to login page if not authenticated
        
        agent_ips, agent_names = get_agent_ips_and_names() 
        agent_options = ['{} - {}'.format(ip, name) for ip, name in zip(agent_ips, agent_names)]
        return render_template('index.html', agent_options=agent_options, predefined_rules=predefined_rules_list)
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        return "An error occurred while loading the page."

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth_key = request.form['auth_key']
        # Replace 'YOUR_AUTH_KEY' with your actual authentication key/token
        if auth_key == AUTH_KEY:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid authentication key'
    return render_template('login.html')
# Logout route (optional)
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))


# Decorator function to require authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))  # Redirect to login page if not authenticated
        return f(*args, **kwargs)
    return decorated_function

# agent selection function
@app.route('/select_agent', methods=['POST'])
@login_required
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

#inbound rule function
@app.route('/inbound-rules', methods=['POST'])
@login_required
def apply_inbound_rule():
    try:
        inbound_rule = request.json.get('inbound_rule')
        logger.info("Received inbound rule data: %s", inbound_rule)  # Log 
        
        if inbound_rule:
            # Log AGENT_URL
            logger.info("Sending request to AGENT_URL: %s", session.get("AGENT_URL"))
            logger.info("Request payload: %s", request.json)
            response = requests.post(f'{session.get("AGENT_URL")}/inbound_rule', json={'inbound_rule': inbound_rule})
            # Log the response
            if response.status_code == 200:
                logging.info("Response from agent: %s", response.json())
            else:
                logging.error("Error response from agent: %s", response.status_code)
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
    
#OutBound Function
@app.route('/outbound-rules', methods=['POST'])
@login_required
def apply_outbound_rule():
    try:
        outbound_rule = request.json.get('outbound_rule')
        logger.info("Received inbound rule data: %s", outbound_rule)  # Log the received data
        
        if outbound_rule:
            # Log AGENT_URL
            logger.info("Sending request to AGENT_URL: %s", session.get("AGENT_URL"))
            logger.info("Request payload: %s", request.json)
            response = requests.post(f'{session.get("AGENT_URL")}/outbound_rule', json={'outbound_rule': outbound_rule})
            # Log  response 
            if response.status_code == 200:
                logging.info("Response from agent: %s", response.json())
            else:
                logging.error("Error response from agent: %s", response.status_code)
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
    
#Bloack Port separate function
@app.route('/block_port', methods=['GET', 'POST'])
@login_required
def block_port():
    if request.method == 'POST':
        try:
            port = request.form.get('portNumber')
            if not port:
                return jsonify({'error': 'Port number is required'}), 400

            payload = {'port': port}
            response = requests.post(f'{session.get("AGENT_URL")}/block_port', json=payload)

            if response.status_code == 200:
                return jsonify({'message': f'Port {port} blocked successfully'}), 200
            else:
                return jsonify({'error': response.text}), response.status_code
        except Exception as e:
            logger.error("An error occurred while blocking port: %s", str(e))
            return jsonify({'error': 'An error occurred while blocking port.'}), 500
    elif request.method == 'GET':
        return render_template('block_port.html')

@app.route('/add_agent')
@login_required
def add_ageents():
    agents = agents_collections.find()
    return render_template('add_agent.html', agents=agents)

# add agent function
@app.route('/add', methods=['POST','GET'])
@login_required
def add_agent():
    try:
        agent_id = request.form.get('agent_id')
        agent_name = request.form.get('agent_name')
        status = request.form.get('status')
        ip_address = request.form.get('ip_address')
        
        if agent_id is None or agent_name is None or status is None or ip_address is None:

            return 'Missing required fields', 400
        
        agents_collections.insert_one({'agent_id': agent_id, 'agent_name': agent_name, 'status': status, 'ip_address': ip_address})
        
        return redirect(url_for('add_agent'))
    except Exception as e:
        return str(e), 400

@app.errorhandler(Exception)
@login_required
def handle_error(e):
    logger.error("An unexpected error occurred: %s", str(e))
    return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/rule_manager',methods=['POST','GET'])
@login_required
def rule_manager():
    return render_template('manage_rules.html')

#agent downloader 
@app.route('/download_agent',methods=['POST','GET'])
@login_required
def download_agent():
    return  render_template("download_agent.html")

# @app.route('/download-file')
# def download_file():
#     try:
#         zip_file_path = './agent_file/agent.tar'
#         if not os.path.isfile(zip_file_path):
#             return "The requested file does not exist.", 404
#         filename = 'agent.tar'
#         response = make_response(send_file(zip_file_path, as_attachment=True))
#         response.headers['Content-Type'] = 'application/octet-stream'
#         response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
#         return response
#     except Exception as e:
#         logging.error(f"An error occurred while downloading the file: {str(e)}")
#         return "An error occurred while downloading the file. Please try again later.", 500

#flush rules function
@app.route('/flush_rules', methods=['GET','POST'])
@login_required
def flush_rules():
    if 'AGENT_URL' in session:
        try:
            response = requests.post(f'{session.get("AGENT_URL")}/flush')
            return response.text, response.status_code
        except requests.exceptions.RequestException as e:
            return str(e), 500
    else:
        return 'Agent URL not set in session.', 400

#show rules function
@app.route('/show_rules', methods=['GET','POST'])
@login_required
def show_rules():
    if 'AGENT_URL' in session:
        try:
            response = requests.get(f'{session.get("AGENT_URL")}/show_rules')
            return response.text, response.status_code
        except requests.exceptions.RequestException as e:
            return str(e), 500
    else:
        return 'Agent URL not set in session.', 400
    

if __name__ == "__main__":
    app.run(debug=True,port=7000)