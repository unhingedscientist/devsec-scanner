"""
App installation and configuration management for DevSec Scanner GitHub App
"""
import os
import yaml

def load_app_config(path='app-config.yml'):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def save_app_config(config, path='app-config.yml'):
    with open(path, 'w') as f:
        yaml.safe_dump(config, f)
