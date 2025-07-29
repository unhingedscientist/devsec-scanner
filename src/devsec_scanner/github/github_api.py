"""
GitHub API integration for repository analysis and PR comments
"""
import os
import requests
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_API = 'https://api.github.com'

def get_repo_info(repo):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    resp = requests.get(f'{GITHUB_API}/repos/{repo}', headers=headers)
    resp.raise_for_status()
    return resp.json()

def post_pr_comment(repo, pr_number, body):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f'{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments'
    resp = requests.post(url, headers=headers, json={'body': body})
    resp.raise_for_status()
    return resp.json()
