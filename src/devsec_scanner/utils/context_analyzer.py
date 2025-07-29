"""
context_analyzer.py
Extracts context and computes confidence for detected secrets.
"""
from typing import List, Dict, Any

CONTEXT_LINES = 2


def extract_context(lines: List[str], line_number: int) -> str:
    start = max(0, line_number - 1 - CONTEXT_LINES)
    end = min(len(lines), line_number + CONTEXT_LINES)
    return '\n'.join(lines[start:end])


def score_confidence(entropy: float, base64: bool, pattern_conf: float) -> int:
    score = 0
    if entropy > 4.5:
        score += 60
    if base64:
        score += 20
    if pattern_conf > 0.9:
        score += 20
    elif pattern_conf > 0.8:
        score += 10
    return min(score, 100)


def analyze_secret(secret: str, line_number: int, lines: List[str], entropy: float, base64: bool, pattern_conf: float) -> Dict[str, Any]:
    context = extract_context(lines, line_number)
    confidence = score_confidence(entropy, base64, pattern_conf)
    return {
        'secret': secret,
        'line': line_number,
        'context': context,
        'entropy': entropy,
        'base64': base64,
        'confidence': confidence
    }

# --- Test function ---
def _test_context_analyzer():
    lines = [
        'foo = "bar"',
        'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"',
        'baz = "qux"',
        'test_secret_key_1234567890',
        'user_id_12345'
    ]
    result = analyze_secret('AKIAIOSFODNN7EXAMPLE', 2, lines, 4.7, False, 0.95)
    assert 'AWS_KEY' in result['context']
    assert result['confidence'] >= 70
    print('[test] context_analyzer.py: PASS')

if __name__ == '__main__':
    _test_context_analyzer()
