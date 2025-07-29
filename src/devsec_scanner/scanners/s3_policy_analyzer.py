"""
S3 bucket policy parsing and vulnerability detection
"""
import json

def analyze_bucket_policy(policy_str):
    """
    Analyze a bucket policy JSON string for overly permissive access.
    Returns a list of findings (dicts with type, severity, description).
    """
    findings = []
    try:
        policy = json.loads(policy_str)
        for stmt in policy.get('Statement', []):
            effect = stmt.get('Effect', '')
            principal = stmt.get('Principal', '')
            actions = stmt.get('Action', [])
            resource = stmt.get('Resource', '')
            if isinstance(actions, str):
                actions = [actions]
            # Detect public read
            if effect == 'Allow' and principal == '*' and 's3:GetObject' in actions:
                findings.append({
                    'type': 'PERMISSIVE_POLICY',
                    'severity': 'HIGH',
                    'description': 'Bucket policy allows public read access.'
                })
            # Detect public write
            if effect == 'Allow' and principal == '*' and (
                's3:PutObject' in actions or 's3:*' in actions):
                findings.append({
                    'type': 'PERMISSIVE_POLICY',
                    'severity': 'CRITICAL',
                    'description': 'Bucket policy allows public write access.'
                })
            # Detect wildcard resource
            if effect == 'Allow' and principal == '*' and resource and (
                resource.endswith('/*') or resource == '*'):
                findings.append({
                    'type': 'PERMISSIVE_POLICY',
                    'severity': 'HIGH',
                    'description': 'Bucket policy allows broad access to all objects.'
                })
    except Exception as e:
        findings.append({
            'type': 'POLICY_PARSE_ERROR',
            'severity': 'LOW',
            'description': f'Error parsing bucket policy: {e}'
        })
    return findings

def test_policy_analyzer():
    print("[TEST] Testing S3 policy analyzer...")
    public_policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::bucket/*"}]}'
    findings = analyze_bucket_policy(public_policy)
    assert any(f['type'] == 'PERMISSIVE_POLICY' for f in findings), "Should detect permissive policy"
    print("[PASS] Policy analyzer detects public read.")
