"""
Branch protection analysis and recommendations for DevSec Scanner GitHub App
"""
import requests

def analyze_branch_protection(repo, token):
    url = f'https://api.github.com/repos/{repo}/branches/main/protection'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.luke-cage-preview+json'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        protection = resp.json()
        recommendations = []
        if not protection.get('required_status_checks', {}).get('strict'):
            recommendations.append('Enable strict status checks')
        if not protection.get('enforce_admins', {}).get('enabled'):
            recommendations.append('Enforce for admins')
        if not protection.get('required_pull_request_reviews', {}).get('required_approving_review_count', 0) >= 2:
            recommendations.append('Require at least 2 approving reviews')
        return {'protection': protection, 'recommendations': recommendations}
    return {'error': 'Could not fetch branch protection'}
