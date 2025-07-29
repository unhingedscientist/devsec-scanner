#!/usr/bin/env python3
"""
Unified CLI for DevSec Scanner with reporting, GitHub, and comparison features
"""
import sys
import argparse
import logging
from src.devsec_scanner.reports.html_reporter import build_html_report
from src.devsec_scanner.reports.json_reporter import build_json_report
from src.devsec_scanner.reports.export_manager import export_html, export_pdf, export_csv
from src.devsec_scanner.reports.report_comparison import compare_reports
from src.devsec_scanner.github.github_api import get_repo_info
from src.devsec_scanner.github.pr_commenter import main as pr_comment_main
from src.devsec_scanner.github.github_workflow import generate_workflow_yaml
from src.devsec_scanner.config.config_manager import load_config
import json
import os

def main():
    parser = argparse.ArgumentParser(description="DevSec Scanner Unified CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Reporting
    report_parser = subparsers.add_parser('report', help='Generate report in various formats')
    report_parser.add_argument('--input', required=True, help='Input scan JSON file')
    report_parser.add_argument('--format', choices=['json','html','pdf','csv'], default='json')
    report_parser.add_argument('--output', required=True, help='Output file')

    # GitHub integration
    github_parser = subparsers.add_parser('github', help='GitHub integration commands')
    github_sub = github_parser.add_subparsers(dest='gh_command', required=True)
    setup_parser = github_sub.add_parser('setup', help='Setup GitHub App integration')
    setup_parser.add_argument('--repo', required=True)
    scan_parser = github_sub.add_parser('scan', help='Scan a GitHub repo or PR')
    scan_parser.add_argument('--repo', required=True)
    scan_parser.add_argument('--pr', type=int)
    workflow_parser = github_sub.add_parser('create-workflow', help='Generate GitHub Actions workflow YAML')
    workflow_parser.add_argument('--output', required=True)

    # Report comparison
    compare_parser = subparsers.add_parser('compare', help='Compare two scan reports')
    compare_parser.add_argument('--before', required=True)
    compare_parser.add_argument('--after', required=True)
    compare_parser.add_argument('--output', required=True)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    if args.command == 'report':
        with open(args.input) as f:
            report = json.load(f)
        if args.format == 'json':
            with open(args.output, 'w') as out:
                out.write(json.dumps(report, indent=2))
        elif args.format == 'html':
            export_html(report, args.output)
        elif args.format == 'pdf':
            export_pdf(report, args.output)
        elif args.format == 'csv':
            export_csv(report, args.output)
        print(f"[INFO] Report exported to {args.output}")
    elif args.command == 'github':
        if args.gh_command == 'setup':
            info = get_repo_info(args.repo)
            print(f"[INFO] GitHub repo info: {info}")
        elif args.gh_command == 'scan':
            os.environ['GITHUB_REPOSITORY'] = args.repo
            sys.argv = ['pr_commenter.py', '--report', 'scan-results.json', '--pr', str(args.pr), '--repo', args.repo]
            pr_comment_main()
        elif args.gh_command == 'create-workflow':
            yaml = generate_workflow_yaml()
            with open(args.output, 'w') as f:
                f.write(yaml)
            print(f"[INFO] Workflow YAML written to {args.output}")
    elif args.command == 'compare':
        with open(args.before) as f1, open(args.after) as f2:
            before = json.load(f1)
            after = json.load(f2)
        diff = compare_reports(before, after)
        with open(args.output, 'w') as f:
            json.dump(diff, f, indent=2)
        print(f"[INFO] Comparison report written to {args.output}")

if __name__ == '__main__':
    main()
