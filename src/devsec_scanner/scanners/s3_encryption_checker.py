"""
S3 encryption and security settings validation
"""
def check_bucket_encryption(enc):
    """
    Check if bucket has default encryption enabled.
    Returns a finding if not encrypted.
    """
    findings = []
    if not enc or not enc.get('ServerSideEncryptionConfiguration'):
        findings.append({
            'type': 'NO_ENCRYPTION',
            'severity': 'MEDIUM',
            'description': 'Bucket does not have default encryption enabled.'
        })
    return findings

def test_encryption_checker():
    print("[TEST] Testing S3 encryption checker...")
    findings = check_bucket_encryption(None)
    assert any(f['type'] == 'NO_ENCRYPTION' for f in findings), "Should detect missing encryption"
    print("[PASS] Encryption checker detects missing encryption.")
