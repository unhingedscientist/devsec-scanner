"""
S3 ACL analysis for public permissions
"""
def analyze_bucket_acl(acl):
    """
    Analyze a bucket ACL dict for public access grants.
    Returns a list of findings (dicts with type, severity, description).
    """
    findings = []
    for grant in acl.get('Grants', []):
        grantee = grant.get('Grantee', {})
        permission = grant.get('Permission', '')
        uri = grantee.get('URI', '')
        # Public group URIs
        if uri in [
            'http://acs.amazonaws.com/groups/global/AllUsers',
            'http://acs.amazonaws.com/groups/global/AuthenticatedUsers']:
            if permission == 'READ':
                findings.append({
                    'type': 'PUBLIC_ACL',
                    'severity': 'HIGH',
                    'description': 'ACL grants public READ access.'
                })
            if permission == 'WRITE':
                findings.append({
                    'type': 'PUBLIC_ACL',
                    'severity': 'CRITICAL',
                    'description': 'ACL grants public WRITE access.'
                })
            if permission == 'FULL_CONTROL':
                findings.append({
                    'type': 'PUBLIC_ACL',
                    'severity': 'CRITICAL',
                    'description': 'ACL grants public FULL CONTROL.'
                })
    return findings

def test_acl_scanner():
    print("[TEST] Testing S3 ACL scanner...")
    acl = {'Grants': [{
        'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'},
        'Permission': 'READ'
    }]}
    findings = analyze_bucket_acl(acl)
    assert any(f['type'] == 'PUBLIC_ACL' for f in findings), "Should detect public ACL"
    print("[PASS] ACL scanner detects public read.")
