"""
entropy_detector.py
Shannon entropy and base64 detection for secret validation.
"""
import math
import re
from typing import Optional

UUID_REGEX = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
HEX_HASH_REGEX = re.compile(r"\b[a-fA-F0-9]{32,64}\b")
TIMESTAMP_REGEX = re.compile(r"\b1[5-9][0-9]{8,}\b")

BASE64_REGEX = re.compile(r"^[A-Za-z0-9+/=]{20,}$")

ENTROPY_THRESHOLD = 4.5
BASE64_MIN_LENGTH = 20


def shannon_entropy(data: str) -> float:
    if not data:
        return 0.0
    freq = {}
    for c in data:
        freq[c] = freq.get(c, 0) + 1
    entropy = 0.0
    for c in freq:
        p = freq[c] / len(data)
        entropy -= p * math.log2(p)
    return entropy

def is_base64(s: str) -> bool:
    return bool(BASE64_REGEX.match(s))

def is_false_positive(s: str) -> bool:
    if UUID_REGEX.match(s):
        return True
    if HEX_HASH_REGEX.match(s):
        return True
    if TIMESTAMP_REGEX.match(s):
        return True
    return False

def validate_secret(candidate: str) -> Optional[dict]:
    entropy = shannon_entropy(candidate)
    base64 = is_base64(candidate)
    if is_false_positive(candidate):
        return None
    confidence = 0
    if entropy > ENTROPY_THRESHOLD:
        confidence += 60
    if base64:
        confidence += 30
    if len(candidate) > 20:
        confidence += 10
    if confidence < 70:
        return None
    return {
        'secret': candidate,
        'entropy': entropy,
        'base64': base64,
        'confidence': confidence
    }

# --- Test function ---
def _test_entropy_detector():
    assert shannon_entropy('test_secret_key_1234567890') > 4.5
    assert not validate_secret('user_id_12345')
    assert not validate_secret('550e8400-e29b-41d4-a716-446655440000')
    assert validate_secret('test_secret_key_1234567890')
    print('[test] entropy_detector.py: PASS')

if __name__ == '__main__':
    _test_entropy_detector()
