"""
Main CLI with AI integration for enhanced reporting
"""
import sys
import argparse
import time
from rich.console import Console
from src.devsec_scanner.scanners.firebase_scanner import scan_firebase
from src.devsec_scanner.scanners.git_secrets_scanner import scan_git_secrets
from src.devsec_scanner.scanners.s3_scanner import s3_scan_cli
from src.devsec_scanner.reports.enhanced_reporter import generate_enhanced_report

console = Console()

def main():
    parser = argparse.ArgumentParser(description="DevSec Scanner with AI-enhanced reporting")
    parser.add_argument('scanner', choices=['firebase', 'git', 's3'], help='Scanner type')
    parser.add_argument('--path', '-p', help='Target path (file, dir, or repo)')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='Output format')
    parser.add_argument('--env', choices=['prod', 'dev', 'test'], default='prod', help='Environment type')
    parser.add_argument('--compliance', help='Compliance requirements (comma-separated)')
    parser.add_argument('--business-criticality', choices=['high', 'medium', 'low'], default='high')
    args = parser.parse_args()
    start_time = time.time()
    findings = []
    context = {
        'env': args.env,
        'compliance': args.compliance,
        'business_criticality': args.business_criticality
    }
    if args.scanner == 'firebase':
        findings = scan_firebase(path=args.path, output=None, output_format='dict', severity=None)
    elif args.scanner == 'git':
        findings = scan_git_secrets(path=args.path, output=None, output_format='dict', severity=None)
    elif args.scanner == 's3':
        # s3_scan_cli handles its own CLI, so here we would call the underlying logic for findings
        from src.devsec_scanner.scanners.s3_enumerator import enumerate_s3_buckets
        from src.devsec_scanner.scanners.s3_vulnerabilities import analyze_s3_bucket
        from src.devsec_scanner.utils.aws_credentials import get_boto3_session, validate_aws_credentials
        from src.devsec_scanner.utils.aws_regions import get_all_aws_regions
        session = get_boto3_session()
        validate_aws_credentials(session)
        owner = 'unknown'
        regions = get_all_aws_regions('s3')
        buckets_by_region = enumerate_s3_buckets(logger=None)
        for region, blist in buckets_by_region.items():
            for b in blist:
                b['Owner'] = owner
                s3 = session.client('s3', region_name=b['Region'])
                findings.extend(analyze_s3_bucket(s3, b['Name']))
    report = generate_enhanced_report(findings, context, fmt=args.format)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
    else:
        console.print(report)
    elapsed = time.time() - start_time
    console.print(f"[bold green]Scan completed in {elapsed:.2f}s")

if __name__ == "__main__":
    main()
