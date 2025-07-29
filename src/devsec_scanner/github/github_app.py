"""
GitHub App core functionality for DevSec Scanner
"""
import os
from flask import Flask, request, jsonify
from src.devsec_scanner.github.webhook_handler import handle_github_event
from src.devsec_scanner.github.app_config import load_app_config

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    config = load_app_config()
    response = handle_github_event(event, payload, config)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
