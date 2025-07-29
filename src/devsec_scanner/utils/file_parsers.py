"""
file_parsers.py
Format-specific content extraction for secret scanning.
"""
import json
import yaml
import re
from typing import List, Dict, Any

def parse_env(content: str) -> List[Dict[str, Any]]:
    results = []
    for i, line in enumerate(content.splitlines(), 1):
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.split('=', 1)
            results.append({'key': k.strip(), 'value': v.strip(), 'line': i})
    return results

def parse_json(content: str) -> List[Dict[str, Any]]:
    try:
        obj = json.loads(content)
    except Exception:
        return []
    results = []
    def walk(obj, path='', line=1):
        if isinstance(obj, dict):
            for k, v in obj.items():
                results.append({'key': k, 'value': v, 'line': line, 'path': path})
                walk(v, path + '.' + k if path else k, line)
        elif isinstance(obj, list):
            for idx, v in enumerate(obj):
                walk(v, f'{path}[{idx}]', line)
    walk(obj)
    return results

def parse_yaml(content: str) -> List[Dict[str, Any]]:
    try:
        obj = yaml.safe_load(content)
    except Exception:
        return []
    results = []
    def walk(obj, path='', line=1):
        if isinstance(obj, dict):
            for k, v in obj.items():
                results.append({'key': k, 'value': v, 'line': line, 'path': path})
                walk(v, path + '.' + k if path else k, line)
        elif isinstance(obj, list):
            for idx, v in enumerate(obj):
                walk(v, f'{path}[{idx}]', line)
    walk(obj)
    return results

def parse_text(content: str) -> List[Dict[str, Any]]:
    # For .txt, .md, .py, .js, just return lines
    return [{'key': None, 'value': line, 'line': i+1} for i, line in enumerate(content.splitlines())]

# --- Test function ---
def _test_file_parsers():
    env = 'AWS_KEY=AKIAIOSFODNN7EXAMPLE\n# Comment\nUSER=admin'
    assert any('AKIA' in d['value'] for d in parse_env(env))
    js = '{"apiKey": "AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI"}'
    assert any('AIza' in d['value'] for d in parse_json(js))
    yml = 'api_key: ghp_1234567890abcdef1234567890abcdef123456'
    assert any('ghp_' in d['value'] for d in parse_yaml(yml))
    print('[test] file_parsers.py: PASS')

if __name__ == '__main__':
    _test_file_parsers()
