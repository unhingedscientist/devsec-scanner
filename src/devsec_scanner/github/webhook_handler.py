"""
Repository webhook processing for DevSec Scanner GitHub App
"""
from src.devsec_scanner.github.branch_protection import analyze_branch_protection
from src.devsec_scanner.github.github_api import get_repo_info

def handle_github_event(event, payload, config):
    if event == 'push':
        # Trigger scan, update status
        repo = payload['repository']['full_name']
        return {'status': 'scan triggered', 'repo': repo}
    if event == 'pull_request':
        # Scan PR, comment, update status
        pr = payload['pull_request']['number']
        repo = payload['repository']['full_name']
        return {'status': 'pr scan triggered', 'repo': repo, 'pr': pr}
    if event == 'repository':
        # Handle repo config changes
        repo = payload['repository']['full_name']
        return {'status': 'repo config updated', 'repo': repo}
    if event == 'installation':
        # App installed/uninstalled
        return {'status': 'installation event'}
    if event == 'security_advisory':
        # Track security advisories
        return {'status': 'security advisory received'}
    return {'status': 'event ignored'}
