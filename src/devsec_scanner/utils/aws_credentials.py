"""
AWS Credentials detection and session management for DevSec Scanner
"""
import os
import boto3
import botocore
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ProfileNotFound

def get_boto3_session(profile_name=None, credentials_path=None):
    """
    Detect AWS credentials in the following order:
    1. Environment variables
    2. ~/.aws/credentials profile (optionally custom path)
    3. IAM instance profile
    4. Assume role if configured in profile
    Returns a boto3.Session or raises an error.
    """
    # 1. Environment variables
    if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
        return boto3.Session()
    # 2. Profile (optionally custom path)
    if profile_name or credentials_path:
        session_kwargs = {}
        if profile_name:
            session_kwargs['profile_name'] = profile_name
        if credentials_path:
            os.environ['AWS_SHARED_CREDENTIALS_FILE'] = credentials_path
        try:
            return boto3.Session(**session_kwargs)
        except ProfileNotFound as e:
            raise RuntimeError(f"AWS profile not found: {profile_name}") from e
    # 3. IAM instance profile or default
    try:
        return boto3.Session()
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise RuntimeError("No valid AWS credentials found.") from e

def validate_aws_credentials(session):
    """
    Validate that the session has working credentials by calling sts:GetCallerIdentity.
    Returns the caller identity dict or raises an error.
    """
    try:
        sts = session.client('sts')
        return sts.get_caller_identity()
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"Invalid AWS credentials: {e}")
    except Exception as e:
        raise RuntimeError(f"Error validating AWS credentials: {e}")

def test_aws_credentials():
    print("[TEST] Testing AWS credential detection...")
    try:
        session = get_boto3_session()
        ident = validate_aws_credentials(session)
        print(f"[PASS] AWS credentials valid: {ident['Arn']}")
    except Exception as e:
        print(f"[FAIL] {e}")
