# rule_manager.py
from flask import request, jsonify
import requests
import logging

logger = logging.getLogger(__name__)

def apply_inbound_rule(session):
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

def apply_outbound_rule(session):
    try:
        outbound_rule = request.json.get('outbound_rule')
        logger.info("Received outbound rule data: %s", outbound_rule)  # Log the received data
        
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
                return jsonify({'message': 'Outbound rule applied successfully to the agent'}), 200
            else:
                return jsonify({'error': 'Error applying outbound rule to the agent'}), 500
        else:
            return jsonify({'error': 'No outbound rule provided'}), 400
    except requests.RequestException as e:
        logger.error("Error occurred while sending request to agent server: %s", str(e))
        return jsonify({'error': 'Error sending request to the agent server'}), 500
    except Exception as e:
        logger.error("An unexpected error occurred while applying outbound rule: %s", str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500
