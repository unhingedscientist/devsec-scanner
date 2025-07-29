"""
Pull request comment functionality for DevSec Scanner
"""
import sys
import json
import os
from src.devsec_scanner.github.github_api import post_pr_comment

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', required=True)
    parser.add_argument('--pr', required=True)
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    args = parser.parse_args()
    with open(args.report) as f:
        report = json.load(f)
    summary = f"Security scan: {report['summary']['total_findings']} findings. Score: {report['summary']['security_score']}\n"
    for f in report['findings'][:5]:
        summary += f"- [{f['severity']}] {f['title']}: {f['description']}\n"
    post_pr_comment(args.repo, args.pr, summary)

if __name__ == '__main__':
    main()
