"""
Comprehensive S3 vulnerability reporting with remediation steps
"""
REMEDIATION_MAP = {
    'NO_ENCRYPTION': "Enable default encryption: aws s3api put-bucket-encryption --bucket <bucket> --server-side-encryption-configuration ...",
    'PUBLIC_ACCESS_BLOCK_DISABLED': "Block public access: aws s3api put-public-access-block --bucket <bucket> --public-access-block-configuration ...",
    'PERMISSIVE_POLICY': "Review bucket policy: Remove wildcard principals or actions.",
    'PUBLIC_ACL': "Remove public grants from ACL: aws s3api put-bucket-acl ...",
    'PUBLIC_READ': "Restrict public read: Remove 's3:GetObject' for Principal '*'.",
    'PUBLIC_WRITE': "Restrict public write: Remove 's3:PutObject' for Principal '*'.",
    'LOGGING_DISABLED': "Enable logging: aws s3api put-bucket-logging ...",
    'VERSIONING_DISABLED': "Enable versioning: aws s3api put-bucket-versioning ...",
    'MFA_DELETE_DISABLED': "Enable MFA Delete: aws s3api put-bucket-versioning ...",
}

def generate_report(findings, bucket_meta):
    """
    Generate a detailed report for a bucket's findings.
    Returns a list of dicts with all required fields.
    """
    report = []
    for f in findings:
        remediation = REMEDIATION_MAP.get(f['type'], 'Review AWS documentation for remediation.')
        risk_score = {'CRITICAL': 10, 'HIGH': 8, 'MEDIUM': 5, 'LOW': 2}.get(f['severity'], 1)
        report.append({
            'bucket': bucket_meta.get('Name'),
            'region': bucket_meta.get('Region'),
            'owner': bucket_meta.get('Owner', 'unknown'),
            'vulnerability': f['type'],
            'severity': f['severity'],
            'details': f.get('description', ''),
            'permissions': bucket_meta.get('Policy', ''),
            'remediation': remediation,
            'risk_score': risk_score
        })
    return report

def test_s3_reporter():
    print("[TEST] S3 reporter test...")
    findings = [
        {'type': 'NO_ENCRYPTION', 'severity': 'MEDIUM', 'description': 'No encryption.'},
        {'type': 'PUBLIC_ACL', 'severity': 'HIGH', 'description': 'ACL grants public read.'}
    ]
    meta = {'Name': 'bucket', 'Region': 'us-east-1', 'Owner': '1234567890', 'Policy': '{...}'}
    report = generate_report(findings, meta)
    assert any(r['remediation'] for r in report), "Remediation should be present"
    print("[PASS] S3 reporter generates remediation.")
