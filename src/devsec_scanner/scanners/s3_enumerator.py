"""
S3 bucket enumeration with multi-region support, robust error handling, and retry logic
"""
import time
import random
import logging
import botocore
from botocore.exceptions import ClientError, EndpointConnectionError
from src.devsec_scanner.utils.aws_credentials import get_boto3_session
from src.devsec_scanner.utils.aws_regions import get_all_aws_regions, validate_regions

MAX_RETRIES = 5
BACKOFF_BASE = 1.5


def exponential_backoff(retries):
    return BACKOFF_BASE ** retries + random.uniform(0, 1)

def enumerate_s3_buckets(profile_name=None, credentials_path=None, regions=None, logger=None):
    """
    Enumerate S3 buckets across all or specified AWS regions.
    Returns: dict {region: [bucket_metadata, ...]}
    """
    session = get_boto3_session(profile_name, credentials_path)
    if not regions:
        regions = get_all_aws_regions('s3')
    else:
        regions = validate_regions(regions, 's3')
    results = {}
    for region in regions:
        region_buckets = []
        retries = 0
        while retries < MAX_RETRIES:
            try:
                s3 = session.client('s3', region_name=region)
                paginator = s3.get_paginator('list_buckets')
                for page in paginator.paginate():
                    for bucket in page.get('Buckets', []):
                        # Get bucket location
                        try:
                            loc = s3.get_bucket_location(Bucket=bucket['Name'])
                            bucket_region = loc.get('LocationConstraint') or 'us-east-1'
                        except ClientError:
                            bucket_region = 'unknown'
                        # Only include if in this region
                        if bucket_region == region:
                            meta = {
                                'Name': bucket['Name'],
                                'CreationDate': str(bucket['CreationDate']),
                                'Region': bucket_region
                            }
                            region_buckets.append(meta)
                break  # Success, exit retry loop
            except EndpointConnectionError as e:
                if logger:
                    logger.warning(f"[S3] Network error in {region}: {e}, retrying...")
                time.sleep(exponential_backoff(retries))
                retries += 1
            except ClientError as e:
                code = e.response['Error']['Code']
                if code in ('Throttling', 'RequestLimitExceeded', 'SlowDown'):
                    if logger:
                        logger.warning(f"[S3] Rate limited in {region}: {code}, retrying...")
                    time.sleep(exponential_backoff(retries))
                    retries += 1
                elif code in ('AccessDenied', 'UnauthorizedOperation'):
                    if logger:
                        logger.error(f"[S3] Permission denied in {region}: {code}")
                    break
                elif code in ('InvalidAccessKeyId', 'SignatureDoesNotMatch'):
                    if logger:
                        logger.error(f"[S3] Invalid credentials in {region}: {code}")
                    break
                else:
                    if logger:
                        logger.error(f"[S3] Client error in {region}: {e}")
                    break
            except Exception as e:
                if logger:
                    logger.error(f"[S3] Unexpected error in {region}: {e}")
                break
        results[region] = region_buckets
    return results

def test_s3_enumerator():
    import logging
    logger = logging.getLogger("s3_enum_test")
    logger.setLevel(logging.INFO)
    print("[TEST] Testing S3 enumeration...")
    try:
        results = enumerate_s3_buckets(logger=logger)
        for region, buckets in results.items():
            print(f"Region: {region}, Buckets: {len(buckets)}")
        print("[PASS] S3 enumeration completed.")
    except Exception as e:
        print(f"[FAIL] {e}")
