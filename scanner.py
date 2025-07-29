#!/usr/bin/env python3
"""
DevSec Scanner unified CLI
Usage:
  ./scanner [firebase|git|s3] --path <target> [--output <file>] [--format <json|text>] [--severity <level>]
"""
import sys
import os
import argparse
import time
import logging
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from src.devsec_scanner.scanners.firebase_scanner import scan_firebase
from src.devsec_scanner.scanners.git_secrets_scanner import scan_git_secrets
from src.devsec_scanner.scanners.s3_scanner import s3_scan_cli

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="DevSec Scanner: Unified Security Scanning CLI"
    )
    subparsers = parser.add_subparsers(dest="scanner", required=True, help="Scanner type")

    # Common arguments
    def add_common_args(p):
        p.add_argument('--path', '-p', required=False, help='Target path (file, directory, or repo)')
        p.add_argument('--output', '-o', help='Output file (default: stdout)')
        p.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='Output format')
        p.add_argument('--severity', '-s', choices=['low', 'medium', 'high'], help='Minimum severity to report')

    # Firebase subcommand
    parser_firebase = subparsers.add_parser('firebase', help='Scan Firebase project/rules')
    add_common_args(parser_firebase)

    # Git subcommand
    parser_git = subparsers.add_parser('git', help='Scan Git repository for secrets')
    add_common_args(parser_git)

    # S3 subcommand
    parser_s3 = subparsers.add_parser('s3', help='Scan AWS S3 buckets for security issues')
    parser_s3.add_argument('--profile', help='AWS profile name')
    parser_s3.add_argument('--region', action='append', help='Target AWS region(s)')
    parser_s3.add_argument('--bucket-name', help='Scan a specific bucket only')
    parser_s3.add_argument('--check-encryption', action='store_true', help='Check for encryption only')
    parser_s3.add_argument('--format', choices=['text', 'json', 'csv'], default='text', help='Output format')
    parser_s3.add_argument('--output', help='Export results to file')

    args = parser.parse_args()
    start_time = time.time()
    exit_code = 0
    try:
        if args.scanner == 'firebase':
            with Progress() as progress:
                task = progress.add_task("[cyan]Scanning Firebase...", total=1)
                results = scan_firebase(
                    path=args.path,
                    output=args.output,
                    output_format=args.format,
                    severity=args.severity,
                    progress=progress,
                    task=task
                )
                progress.update(task, advance=1)
            # Output handling
            if args.output:
                with open(args.output, 'w') as f:
                    if args.format == 'json':
                        import json
                        json.dump(results, f, indent=2)
                    else:
                        f.write(results if isinstance(results, str) else str(results))
            else:
                if args.format == 'json':
                    import json
                    console.print_json(data=results)
                else:
                    console.print(results)
            # Exit code logic
            if results and (isinstance(results, dict) and results.get('findings')):
                exit_code = 1
            elif results and isinstance(results, list) and len(results) > 0:
                exit_code = 1
            else:
                exit_code = 0
        elif args.scanner == 'git':
            with Progress() as progress:
                task = progress.add_task("[magenta]Scanning Git repo...", total=1)
                results = scan_git_secrets(
                    path=args.path,
                    output=args.output,
                    output_format=args.format,
                    severity=args.severity,
                    progress=progress,
                    task=task
                )
                progress.update(task, advance=1)
            # Output handling
            if args.output:
                with open(args.output, 'w') as f:
                    if args.format == 'json':
                        import json
                        json.dump(results, f, indent=2)
                    else:
                        f.write(results if isinstance(results, str) else str(results))
            else:
                if args.format == 'json':
                    import json
                    console.print_json(data=results)
                else:
                    console.print(results)
            # Exit code logic
            if results and (isinstance(results, dict) and results.get('findings')):
                exit_code = 1
            elif results and isinstance(results, list) and len(results) > 0:
                exit_code = 1
            else:
                exit_code = 0
        elif args.scanner == 's3':
            # Delegate to s3_scan_cli for full argument parsing and reporting
            s3_scan_cli()
            return  # s3_scan_cli handles sys.exit
        else:
            parser.print_help()
            sys.exit(2)
    except Exception as e:
        logging.error(f"Error: {e}")
        exit_code = 2
    finally:
        elapsed = time.time() - start_time
        console.print(f"[bold green]Scan completed in {elapsed:.2f}s")
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
