"""
git_secrets_scanner.py
Main CLI entry point for Git secrets scanning.
"""
import os
import sys
from typing import List, Dict, Any
from rich.progress import Progress
from ..utils.file_traversal import scan_files
from ..utils.secret_patterns import find_secrets_in_text
from ..utils.entropy_detector import validate_secret
from ..utils.file_parsers import parse_env, parse_json, parse_yaml, parse_text
from ..utils.context_analyzer import analyze_secret
from ..utils.whitelist_manager import WhitelistManager
from .secrets_reporter import report_secrets

FILE_PARSERS = {
    '.env': parse_env,
    '.json': parse_json,
    '.yaml': parse_yaml,
    '.yml': parse_yaml,
    '.txt': parse_text,
    '.md': parse_text,
    '.py': parse_text,
    '.js': parse_text,
}


def scan_git_secrets(path: str) -> int:
    wm = WhitelistManager(path)
    findings: List[Dict[str, Any]] = []
    files = list(scan_files(path))
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning for secrets...", total=len(files))
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            parser = FILE_PARSERS.get(ext, parse_text)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                progress.update(task, advance=1)
                continue
            lines = content.splitlines()
            for item in parser(content):
                value = str(item.get('value', ''))
                line_num = item.get('line', 1)
                line = lines[line_num-1] if 0 < line_num <= len(lines) else ''
                if wm.is_ignored(file_path, line, value):
                    continue
                for match in find_secrets_in_text(value, file_path):
                    if wm.is_ignored(file_path, line, match['value']):
                        continue
                    v = validate_secret(match['value'])
                    if not v:
                        continue
                    analyzed = analyze_secret(
                        match['value'],
                        line_num,
                        lines,
                        v['entropy'],
                        v['base64'],
                        match['confidence']
                    )
                    analyzed.update({
                        'file': file_path,
                        'line': line_num,
                        'type': match['type'],
                        'confidence': analyzed['confidence'],
                        'severity': 'HIGH' if analyzed['confidence'] > 90 else 'MEDIUM' if analyzed['confidence'] > 80 else 'LOW',
                        'advice': 'Rotate secret and remove from code.'
                    })
                    findings.append(analyzed)
            progress.update(task, advance=1)
    report_secrets(findings)
    return 0 if not findings else 1

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Git Secrets Scanner")
    parser.add_argument('path', nargs='?', default='.', help='Path to Git repo directory')
    args = parser.parse_args()
    sys.exit(scan_git_secrets(args.path))

# --- Test function ---
def _test_end_to_end():
    import tempfile, shutil
    tempdir = tempfile.mkdtemp()
    try:
        with open(os.path.join(tempdir, 'test.env'), 'w') as f:
            f.write('AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n# secretsignore\nUSER=admin')
        with open(os.path.join(tempdir, '.secretsignore'), 'w') as f:
            f.write('USER=admin\n')
        rc = scan_git_secrets(tempdir)
        assert rc == 0
        print('[test] git_secrets_scanner.py: PASS')
    finally:
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    main()
