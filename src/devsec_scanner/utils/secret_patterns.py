"""
secret_patterns.py
Comprehensive regex patterns for secret detection with confidence scoring.
"""
import re
from typing import List, Dict, Any

SECRET_PATTERNS = [
    # AWS Access Key ID
    {"name": "AWS Access Key", "pattern": r"AKIA[0-9A-Z]{16}", "confidence": 0.95},
    {"name": "AWS Secret Key", "pattern": r"(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])", "confidence": 0.90},
    {"name": "AWS Session Key", "pattern": r"ASIA[0-9A-Z]{16}", "confidence": 0.95},
    # Google API Key
    {"name": "Google API Key", "pattern": r"AIza[0-9A-Za-z-_]{35,}", "confidence": 0.95},
    # GitHub tokens
    {"name": "GitHub Token", "pattern": r"gh[pso]_[A-Za-z0-9]{36,}", "confidence": 0.95},
    # Database connection strings
    {"name": "MongoDB URI", "pattern": r"mongodb://[\w\d:%@\-\.]+", "confidence": 0.95},
    {"name": "Postgres URI", "pattern": r"postgres://[\w\d:%@\-\.]+", "confidence": 0.95},
    {"name": "MySQL URI", "pattern": r"mysql://[\w\d:%@\-\.]+", "confidence": 0.95},
    # JWT tokens
    {"name": "JWT Token", "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "confidence": 0.90},
    # Private keys
    {"name": "Private Key", "pattern": r"-----BEGIN (RSA|DSA|EC|OPENSSH|PRIVATE) KEY-----", "confidence": 0.99},
    # Generic API Key
    {"name": "Generic API Key", "pattern": r"(?i)(api|access|secret|token|key)[\s:=\"]{1,10}[A-Za-z0-9\-_=]{16,}", "confidence": 0.80},
]

def find_secrets_in_text(text: str, file_path: str) -> List[Dict[str, Any]]:
    findings = []
    for pat in SECRET_PATTERNS:
        for match in re.finditer(pat["pattern"], text):
            findings.append({
                "type": pat["name"],
                "value": match.group(0),
                "file": file_path,
                "line": text[:match.start()].count('\n') + 1,
                "confidence": pat["confidence"]
            })
    return findings

# --- Test function ---
def _test_secret_patterns():
    samples = [
        ("AKIAIOSFODNN7EXAMPLE", "AWS Access Key"),
        ("AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI", "Google API Key"),
        ("ghp_1234567890abcdef1234567890abcdef123456", "GitHub Token"),
        ("mongodb://user:pass@host:27017/db", "MongoDB URI"),
        ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c", "JWT Token"),
        ("-----BEGIN PRIVATE KEY-----", "Private Key"),
        ("api_key = 'sk-1234567890abcdef'", "Generic API Key"),
    ]
    for text, expected in samples:
        found = find_secrets_in_text(text, 'test.txt')
        assert any(f['type'] == expected for f in found), f"Failed to detect {expected}"
    print('[test] secret_patterns.py: PASS')

if __name__ == '__main__':
    _test_secret_patterns()
