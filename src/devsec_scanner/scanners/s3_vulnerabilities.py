"""
S3 bucket vulnerability detection orchestrator
"""
import logging
import botocore
from src.devsec_scanner.scanners.s3_policy_analyzer import analyze_bucket_policy
from src.devsec_scanner.scanners.s3_acl_scanner import analyze_bucket_acl
from src.devsec_scanner.scanners.s3_encryption_checker import check_bucket_encryption

def analyze_s3_bucket(s3_client, bucket_name):
    """
    Analyze a single S3 bucket for security misconfigurations.
    Returns: list of findings (dicts)
    """
    findings = []
    # 1. Public access block
    try:
        pab = s3_client.get_public_access_block(Bucket=bucket_name)
        pab_cfg = pab.get('PublicAccessBlockConfiguration', {})
        if not pab_cfg.get('BlockPublicAcls', True) or not pab_cfg.get('BlockPublicPolicy', True):
            findings.append({
                'type': 'PUBLIC_ACCESS_BLOCK_DISABLED',
                'severity': 'HIGH',
                'description': 'Public access block is disabled.'
            })
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchPublicAccessBlockConfiguration':
            findings.append({
                'type': 'PUBLIC_ACCESS_BLOCK_ERROR',
                'severity': 'LOW',
                'description': f'Error checking public access block: {e}'
            })
    # 2. Bucket policy
    try:
        pol = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy_str = pol['Policy']
        findings += analyze_bucket_policy(policy_str)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
            findings.append({
                'type': 'POLICY_ERROR',
                'severity': 'LOW',
                'description': f'Error retrieving bucket policy: {e}'
            })
    # 3. ACL
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        findings += analyze_bucket_acl(acl)
    except botocore.exceptions.ClientError as e:
        findings.append({
            'type': 'ACL_ERROR',
            'severity': 'LOW',
            'description': f'Error retrieving bucket ACL: {e}'
        })
    # 4. Encryption
    try:
        enc = s3_client.get_bucket_encryption(Bucket=bucket_name)
        findings += check_bucket_encryption(enc)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            findings += check_bucket_encryption(None)
        else:
            findings.append({
                'type': 'ENCRYPTION_ERROR',
                'severity': 'LOW',
                'description': f'Error retrieving bucket encryption: {e}'
            })
    # 5. Versioning/MFA Delete
    try:
        ver = s3_client.get_bucket_versioning(Bucket=bucket_name)
        if ver.get('Status') != 'Enabled':
            findings.append({
                'type': 'VERSIONING_DISABLED',
                'severity': 'MEDIUM',
                'description': 'Bucket versioning is not enabled.'
            })
        if ver.get('MFADelete') != 'Enabled':
            findings.append({
                'type': 'MFA_DELETE_DISABLED',
                'severity': 'LOW',
                'description': 'MFA Delete is not enabled.'
            })
    except botocore.exceptions.ClientError as e:
        findings.append({
            'type': 'VERSIONING_ERROR',
            'severity': 'LOW',
            'description': f'Error retrieving bucket versioning: {e}'
        })
    # 6. Logging
    try:
        log = s3_client.get_bucket_logging(Bucket=bucket_name)
        if not log.get('LoggingEnabled'):
            findings.append({
                'type': 'LOGGING_DISABLED',
                'severity': 'LOW',
                'description': 'Bucket logging is not enabled.'
            })
    except botocore.exceptions.ClientError as e:
        findings.append({
            'type': 'LOGGING_ERROR',
            'severity': 'LOW',
            'description': f'Error retrieving bucket logging: {e}'
        })
    return findings

def test_s3_vulnerabilities():
    print("[TEST] S3 vulnerability orchestrator test (mocked)")
    class DummyS3:
        def get_public_access_block(self, Bucket):
            return {'PublicAccessBlockConfiguration': {'BlockPublicAcls': False, 'BlockPublicPolicy': True}}
        def get_bucket_policy(self, Bucket):
            return {'Policy': '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::bucket/*"}]}' }
        def get_bucket_acl(self, Bucket):
            return {'Grants': [{'Grantee': {'Type': 'Group', 'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, 'Permission': 'READ'}]}
        def get_bucket_encryption(self, Bucket):
            raise botocore.exceptions.ClientError({'Error': {'Code': 'ServerSideEncryptionConfigurationNotFoundError'}}, 'GetBucketEncryption')
        def get_bucket_versioning(self, Bucket):
            return {'Status': 'Suspended', 'MFADelete': 'Disabled'}
        def get_bucket_logging(self, Bucket):
            return {}
    findings = analyze_s3_bucket(DummyS3(), 'bucket')
    assert any(f['type'] == 'PERMISSIVE_POLICY' for f in findings), "Should detect permissive policy"
    assert any(f['type'] == 'PUBLIC_ACL' for f in findings), "Should detect public ACL"
    assert any(f['type'] == 'NO_ENCRYPTION' for f in findings), "Should detect missing encryption"
    assert any(f['type'] == 'PUBLIC_ACCESS_BLOCK_DISABLED' for f in findings), "Should detect public access block disabled"
    print("[PASS] S3 vulnerability orchestrator detects all issues.")
