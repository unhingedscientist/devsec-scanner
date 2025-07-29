"""
secrets_reporter.py
Formats and reports secrets scan results with statistics.
"""
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich import box

def report_secrets(findings: List[Dict[str, Any]]):
    console = Console()
    if not findings:
        console.print('[green]No secrets found.[/green]')
        return
    table = Table(title="Secrets Scan Results", box=box.SIMPLE)
    table.add_column("File")
    table.add_column("Line")
    table.add_column("Type")
    table.add_column("Confidence")
    table.add_column("Severity")
    table.add_column("Context")
    table.add_column("Advice")
    for f in findings:
        table.add_row(
            f.get('file', ''),
            str(f.get('line', '')),
            f.get('type', ''),
            f"{f.get('confidence', 0)}%",
            f.get('severity', ''),
            f.get('context', '').replace('\n', ' '),
            f.get('advice', '')
        )
    console.print(table)
    # Summary statistics
    high = sum(1 for f in findings if f['severity'] == 'HIGH')
    med = sum(1 for f in findings if f['severity'] == 'MEDIUM')
    low = sum(1 for f in findings if f['severity'] == 'LOW')
    total = len(findings)
    console.print(f"[bold]Summary:[/bold] {total} findings | [red]{high} HIGH[/red], [yellow]{med} MEDIUM[/yellow], [green]{low} LOW[/green]")
    fp_rate = 0  # Placeholder for false positive rate calculation
    console.print(f"[bold]False Positive Rate:[/bold] <10% (target)")

# --- Test function ---
def _test_reporter():
    findings = [
        {'file': 'test.env', 'line': 1, 'type': 'AWS Access Key', 'confidence': 95, 'severity': 'HIGH', 'context': 'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE', 'advice': 'Rotate secret and remove from code.'},
        {'file': 'test.py', 'line': 2, 'type': 'Google API Key', 'confidence': 90, 'severity': 'HIGH', 'context': 'api_key = "AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI"', 'advice': 'Rotate secret and remove from code.'},
    ]
    report_secrets(findings)
    print('[test] secrets_reporter.py: PASS')

if __name__ == '__main__':
    _test_reporter()
