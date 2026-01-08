"""
Flask web application for chatbot deployment
Provides REST API and web interface for the chatbot
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import yaml
import json
import logging
from rasa.core.agent import Agent
from typing import Dict, Any

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
def load_config(config_path: str = "config.yaml") -> Dict:
      """Load YAML configuration"""
      with open(config_path, 'r') as f:
                return yaml.safe_load(f)

  config = load_config()

# Initialize Rasa agent (will be loaded on startup)
agent = None

@app.before_request
def initialize_agent():
      """Initialize Rasa agent on first request"""
      global agent
      if agent is None:
                try:
                              agent = Agent.load("models/default/nlu-INTENT_FEATURIZER_INTENT_CLASSIFIER-ner_crf/")
                              logger.info("Rasa agent loaded successfully")
except Exception as e:
            logger.error(f"Failed to load Rasa agent: {e}")

@app.route('/')
def home():
      """Serve homepage"""
      return render_template('chat.html', title=config['project']['name'])

@app.route('/api/chat', methods=['POST'])
def chat():
      """API endpoint for chatbot conversation"""
      try:
                data = request.json
                user_message = data.get('message', '')

        if not user_message:
                      return jsonify({'error': 'Message is required'}), 400

        if agent is None:
                      return jsonify({'error': 'Chatbot not initialized'}), 500

        # Get response from Rasa agent
        response = agent.handle_parse(user_message)

        return jsonify({
                      'user_message': user_message,
                      'bot_response': response,
                      'success': True
        })

except Exception as e:
        logger.error(f"Error processing message: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
      """Health check endpoint"""
    return jsonify({
              'status': 'healthy',
              'chatbot': config['project']['name'],
              'version': config['project']['version']
    })

@app.route('/api/config', methods=['GET'])
def get_config():
      """Get chatbot configuration"""
    return jsonify({
              'name': config['project']['name'],
              'version': config['project']['version'],
              'domain': config['dataset'].get('domain', 'general')
    })

@app.errorhandler(404)
def not_found(error):
      """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
      """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
      port = config['deployment'].get('port', 5005)
    debug = config['deployment'].get('debug', False)
    app.run(host='0.0.0.0', port=port, debug=debug)
