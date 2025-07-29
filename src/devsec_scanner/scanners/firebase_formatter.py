"""
firebase_formatter.py
Formats Firebase vulnerability reports with colors and structure.
"""
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich import box

SEVERITY_COLORS = {
    'HIGH': 'bold red',
    'MEDIUM': 'yellow',
    'LOW': 'green',
}

def format_vulnerabilities(vulns: List[Dict[str, Any]]):
    console = Console()
    if not vulns:
        console.print('[green]No vulnerabilities found.[/green]')
        return
    table = Table(title="Firebase Vulnerabilities", box=box.SIMPLE)
    table.add_column("Severity", style="bold")
    table.add_column("Title")
    table.add_column("File")
    table.add_column("Line")
    table.add_column("Fix Recommendation")
    for v in vulns:
        color = SEVERITY_COLORS.get(v['severity'], 'white')
        table.add_row(
            f"[{color}]{v['severity']}[/{color}]",
            v['title'],
            v.get('file_path', ''),
            str(v.get('line_number') or ''),
            v.get('fix', '')
        )
    console.print(table)

# --- Test function ---
def _test_formatter():
    vulns = [
        {'severity': 'HIGH', 'title': 'Public read/write', 'file_path': 'firestore.rules', 'line_number': 5, 'fix': 'Restrict access'},
        {'severity': 'MEDIUM', 'title': 'Missing auth', 'file_path': 'firestore.rules', 'line_number': 10, 'fix': 'Add auth check'},
    ]
    format_vulnerabilities(vulns)
    print('[test] firebase_formatter.py: PASS')

if __name__ == '__main__':
    _test_formatter()
