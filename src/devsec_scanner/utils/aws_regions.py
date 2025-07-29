"""
AWS region handling and validation for DevSec Scanner
"""
import boto3
import botocore

def get_all_aws_regions(service_name='s3'):
    """
    Return a list of all AWS regions for a given service (default: s3).
    """
    session = boto3.Session()
    return session.get_available_regions(service_name)

def validate_regions(regions, service_name='s3'):
    """
    Validate a list of region names. Returns only valid regions.
    """
    all_regions = set(get_all_aws_regions(service_name))
    return [r for r in regions if r in all_regions]

def test_aws_regions():
    print("[TEST] Testing AWS region listing...")
    try:
        regions = get_all_aws_regions()
        print(f"[PASS] Found {len(regions)} regions: {regions[:5]} ...")
    except Exception as e:
        print(f"[FAIL] {e}")
