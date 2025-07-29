"""
Severity classification logic for DevSec Scanner
"""
SEVERITY_THRESHOLDS = {
    'CRITICAL': [
        'public data exposure', 'remote code execution', 'admin access', 'public s3 bucket', 'exposed_api_key', 'rce', 'pii exposure'
    ],
    'HIGH': [
        'auth bypass', 'privilege escalation', 'sensitive data access', 'insecure deserialization', 'weak jwt', 'open db'
    ],
    'MEDIUM': [
        'info disclosure', 'weak encryption', 'missing security header', 'directory listing', 'open redirect'
    ],
    'LOW': [
        'version disclosure', 'non-sensitive config', 'best practice', 'info leak', 'banner'
    ]
}

def classify_severity(finding):
    sev = finding.get('severity', '').upper()
    if sev in SEVERITY_THRESHOLDS:
        return sev
    vt = finding.get('vulnerability_type', '').lower()
    desc = finding.get('description', '').lower()
    for level, keywords in SEVERITY_THRESHOLDS.items():
        if any(k in vt or k in desc for k in keywords):
            return level
    return 'LOW'

def test_severity_classifier():
    print("[TEST] Severity classifier...")
    f = {'vulnerability_type': 'public s3 bucket', 'description': 'Bucket is public'}
    assert classify_severity(f) == 'CRITICAL'
    f2 = {'vulnerability_type': 'info disclosure', 'description': 'Header leak'}
    assert classify_severity(f2) == 'MEDIUM'
    print("[PASS] Severity classifier works.")
