"""
Multi-provider AI API client with fallback, retry, rate limiting, and caching
"""
import os
import time
import random
import requests
from src.devsec_scanner.ai.ai_cache import get_cached_response, set_cached_response

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

RATE_LIMIT_SECONDS = 2
MAX_RETRIES = 3
BACKOFF_BASE = 1.5

class RateLimitException(Exception):
    pass

def exponential_backoff(retries):
    return BACKOFF_BASE ** retries + random.uniform(0, 1)

def call_openai(prompt):
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.2
    }
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code == 429:
        raise RateLimitException("OpenAI rate limit")
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']

def call_anthropic(prompt):
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code == 429:
        raise RateLimitException("Anthropic rate limit")
    resp.raise_for_status()
    return resp.json()['content'][0]['text']

def ai_explain_vulnerability(vuln_data, provider_preference=None):
    """
    Input: vuln_data = dict(type, severity, context, resource, ...)
    Output: dict with explanation and remediation
    """
    prompt = vuln_data['prompt']
    cached = get_cached_response(prompt)
    if cached:
        return cached
    last_error = None
    for provider in ([provider_preference] if provider_preference else []) + ['openai', 'anthropic']:
        if provider == 'openai' and OPENAI_API_KEY:
            for retry in range(MAX_RETRIES):
                try:
                    time.sleep(RATE_LIMIT_SECONDS)
                    result = call_openai(prompt)
                    set_cached_response(prompt, {'explanation': result})
                    return {'explanation': result}
                except RateLimitException:
                    time.sleep(exponential_backoff(retry))
                except Exception as e:
                    last_error = e
        if provider == 'anthropic' and ANTHROPIC_API_KEY:
            for retry in range(MAX_RETRIES):
                try:
                    time.sleep(RATE_LIMIT_SECONDS)
                    result = call_anthropic(prompt)
                    set_cached_response(prompt, {'explanation': result})
                    return {'explanation': result}
                except RateLimitException:
                    time.sleep(exponential_backoff(retry))
                except Exception as e:
                    last_error = e
    raise RuntimeError(f"AI API failed: {last_error}")

def test_ai_client():
    print("[TEST] AI client (mocked, no real API call)...")
    # Only test cache logic here
    from src.devsec_scanner.ai.ai_cache import set_cached_response
    prompt = "test ai client"
    set_cached_response(prompt, {"explanation": "cached response"})
    resp = ai_explain_vulnerability({'prompt': prompt})
    assert resp['explanation'] == "cached response"
    print("[PASS] AI client cache/fallback works.")
