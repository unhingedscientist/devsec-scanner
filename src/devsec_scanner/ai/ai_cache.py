"""
Simple in-memory and file-based cache for AI responses
"""
import os
import json
import hashlib

CACHE_DIR = os.path.expanduser('~/.devsecscanner_ai_cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

_memory_cache = {}

def _cache_key(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()

def get_cached_response(prompt):
    key = _cache_key(prompt)
    if key in _memory_cache:
        return _memory_cache[key]
    path = os.path.join(CACHE_DIR, key + '.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            resp = json.load(f)
            _memory_cache[key] = resp
            return resp
    return None

def set_cached_response(prompt, response):
    key = _cache_key(prompt)
    _memory_cache[key] = response
    path = os.path.join(CACHE_DIR, key + '.json')
    with open(path, 'w') as f:
        json.dump(response, f)

def test_ai_cache():
    print("[TEST] AI cache...")
    prompt = "test prompt"
    resp = {"result": "test response"}
    set_cached_response(prompt, resp)
    loaded = get_cached_response(prompt)
    assert loaded == resp
    print("[PASS] AI cache stores and retrieves.")
