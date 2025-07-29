"""
firebase_vulnerabilities.py
Vulnerability checks for Firebase rules and config.
"""
from typing import List, Dict, Any

VULN_SEVERITY = {
    'HIGH': 'HIGH',
    'MEDIUM': 'MEDIUM',
    'LOW': 'LOW',
}

def check_public_read_write(rules_ast: Dict[str, Any], file_path: str) -> List[Dict[str, Any]]:
    vulns = []
    for match in rules_ast.get('matches', []):
        for allow in match.get('allows', []):
            if 'read' in allow['actions'] and 'write' in allow['actions'] and allow['condition'] == 'true':
                vulns.append({
                    'title': 'Public read/write access',
                    'description': 'Rules allow anyone to read and write data.',
                    'severity': VULN_SEVERITY['HIGH'],
                    'file_path': file_path,
                    'line_number': None,
                    'fix': 'Restrict read/write to authenticated users only.'
                })
    return vulns

def check_missing_auth(rules_ast: Dict[str, Any], file_path: str) -> List[Dict[str, Any]]:
    vulns = []
    for match in rules_ast.get('matches', []):
        for allow in match.get('allows', []):
            if 'write' in allow['actions'] and 'request.auth' not in allow['condition']:
                vulns.append({
                    'title': 'Missing authentication on write',
                    'description': 'Write rule does not require authentication.',
                    'severity': VULN_SEVERITY['MEDIUM'],
                    'file_path': file_path,
                    'line_number': None,
                    'fix': 'Require request.auth for write operations.'
                })
    return vulns

def check_broad_permissions(rules_ast: Dict[str, Any], file_path: str) -> List[Dict[str, Any]]:
    vulns = []
    for match in rules_ast.get('matches', []):
        if '**' in match['path']:
            vulns.append({
                'title': 'Overly broad match path',
                'description': f"Match path {match['path']} is too broad.",
                'severity': VULN_SEVERITY['HIGH'],
                'file_path': file_path,
                'line_number': None,
                'fix': 'Avoid using wildcards (**) in match paths.'
            })
    return vulns

def check_hardcoded_secrets(firebase_json: Any, file_path: str) -> List[Dict[str, Any]]:
    vulns = []
    if not firebase_json:
        return vulns
    import re
    json_str = str(firebase_json)
    # Simple regex for API keys
    if re.search(r'AIza[0-9A-Za-z-_]{35,}', json_str):
        vulns.append({
            'title': 'Hardcoded API key',
            'description': 'Potential hardcoded API key found in firebase.json.',
            'severity': VULN_SEVERITY['HIGH'],
            'file_path': file_path,
            'line_number': None,
            'fix': 'Remove hardcoded API keys from config files.'
        })
    return vulns

def run_all_firebase_checks(rules_ast, firebase_json, file_path) -> List[Dict[str, Any]]:
    vulns = []
    vulns += check_public_read_write(rules_ast, file_path)
    vulns += check_missing_auth(rules_ast, file_path)
    vulns += check_broad_permissions(rules_ast, file_path)
    vulns += check_hardcoded_secrets(firebase_json, file_path)
    return vulns

# --- Test function ---
def _test_vuln_checks():
    rules_ast = {
        'matches': [
            {'path': '/{document=**}', 'allows': [{'actions': ['read', 'write'], 'condition': 'true'}]},
            {'path': '/users/{userId}', 'allows': [{'actions': ['write'], 'condition': 'request.auth != null'}]},
            {'path': '/public/{doc}', 'allows': [{'actions': ['write'], 'condition': 'true'}]},
        ]
    }
    firebase_json = {'apiKey': 'AIzaSyDUMMYKEY123456789012345678901234567890'}
    vulns = run_all_firebase_checks(rules_ast, firebase_json, 'firebase.rules')
    assert any(v['severity'] == 'HIGH' for v in vulns)
    print('[test] firebase_vulnerabilities.py: PASS')

if __name__ == '__main__':
    _test_vuln_checks()
