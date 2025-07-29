#!/usr/bin/env python3
"""
Unified DevSec Scanner CLI and scan orchestration
"""
import sys
import os
import argparse
import time
import yaml
import concurrent.futures
from src.devsec_scanner.config.config_manager import load_config
from src.devsec_scanner.scanners.firebase_scanner import scan_firebase
from src.devsec_scanner.scanners.git_secrets_scanner import scan_git_secrets
from src.devsec_scanner.scanners.s3_scanner import s3_scan_cli, s3_scan_logic
from src.devsec_scanner.reports.consolidated_reporter import generate_consolidated_report

SCANNERS = {
    'firebase': scan_firebase,
    'git': scan_git_secrets,
    's3': s3_scan_logic
}


def parse_args():
    parser = argparse.ArgumentParser(description="DevSec Scanner: Unified Security Scanning Platform")
    parser.add_argument('scanners', nargs='+', choices=['firebase', 'git', 's3', 'all'], help='Scanners to run')
    parser.add_argument('--ai-enabled', action='store_true', help='Enable AI explanations and risk scoring')
    parser.add_argument('--output-format', choices=['json', 'text', 'sarif'], default='text', help='Output format')
    parser.add_argument('--severity-filter', choices=['low', 'medium', 'high', 'critical'], help='Minimum severity to report')
    parser.add_argument('--export', help='Export results to file')
    parser.add_argument('--config', default='.scanner-config', help='Path to config file')
    parser.add_argument('--parallel', action='store_true', help='Enable parallel scanning')
    parser.add_argument('--timeout', type=int, default=300, help='Scan timeout (seconds)')
    return parser.parse_args()

def run_scanner(scanner, args, config):
    if scanner == 'firebase':
        return scan_firebase(path=args.get('path'), output=None, output_format='dict', severity=args.get('severity'))
    if scanner == 'git':
        return scan_git_secrets(path=args.get('path'), output=None, output_format='dict', severity=args.get('severity'))
    if scanner == 's3':
        return s3_scan_logic(profile=args.get('profile'), output_format='dict', severity=args.get('severity'))
    return []

def main():
    args = parse_args()
    config = load_config(args.config)
    scanners = ['firebase', 'git', 's3'] if 'all' in args.scanners else args.scanners
    scan_args = {
        'ai_enabled': args.ai_enabled or config.get('ai', {}).get('enabled', False),
        'output_format': args.output_format or config.get('output', {}).get('format', 'text'),
        'severity': args.severity_filter or config.get('output', {}).get('severity_filter'),
        'profile': config.get('scanning', {}).get('profile'),
        'path': config.get('scanning', {}).get('path'),
    }
    start_time = time.time()
    findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(scanners) if args.parallel else 1) as executor:
        future_to_scanner = {executor.submit(run_scanner, s, scan_args, config): s for s in scanners}
        for future in concurrent.futures.as_completed(future_to_scanner, timeout=args.timeout):
            scanner = future_to_scanner[future]
            try:
                result = future.result()
                findings.extend(result)
            except Exception as e:
                print(f"[ERROR] {scanner} scan failed: {e}")
    # Deduplicate and cross-reference
    consolidated = generate_consolidated_report(findings, ai_enabled=scan_args['ai_enabled'], output_format=scan_args['output_format'])
    if args.export:
        with open(args.export, 'w') as f:
            f.write(consolidated)
    else:
        print(consolidated)
    elapsed = time.time() - start_time
    print(f"[bold green]Scan completed in {elapsed:.2f}s")
    # CI/CD exit codes
    if any(f.get('severity', '').lower() in ('high', 'critical') for f in findings):
        sys.exit(1)
    elif findings:
        sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
