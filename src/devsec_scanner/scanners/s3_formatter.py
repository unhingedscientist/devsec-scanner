"""
S3 scan output formatting (JSON, CSV, text)
"""
import json
import csv
from io import StringIO

def format_results(results, fmt='text'):
    if fmt == 'json':
        return json.dumps(results, indent=2)
    elif fmt == 'csv':
        if not results:
            return ''
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=results[0].keys())
        writer.writeheader()
        for row in results:
            writer.writerow(row)
        return output.getvalue()
    else:
        # Pretty text output
        lines = []
        for r in results:
            lines.append(f"Bucket: {r['bucket']} | Region: {r['region']} | Owner: {r['owner']}")
            lines.append(f"  Vulnerability: {r['vulnerability']} | Severity: {r['severity']} | Risk: {r['risk_score']}")
            lines.append(f"  Details: {r['details']}")
            lines.append(f"  Remediation: {r['remediation']}")
            lines.append("")
        return '\n'.join(lines)

def test_s3_formatter():
    print("[TEST] S3 formatter test...")
    results = [{
        'bucket': 'bucket', 'region': 'us-east-1', 'owner': '123',
        'vulnerability': 'NO_ENCRYPTION', 'severity': 'MEDIUM', 'details': 'No encryption.',
        'permissions': '', 'remediation': 'Enable default encryption...', 'risk_score': 5
    }]
    print(format_results(results, 'text'))
    print(format_results(results, 'json'))
    print(format_results(results, 'csv'))
    print("[PASS] S3 formatter outputs all formats.")
