"""
Multi-scanner reporting, deduplication, cross-referencing, SARIF export
"""
import json
import hashlib

def deduplicate_findings(findings):
    seen = set()
    deduped = []
    for f in findings:
        key = hashlib.sha256((f.get('type','')+str(f.get('resource',''))+f.get('description','')).encode()).hexdigest()
        if key not in seen:
            deduped.append(f)
            seen.add(key)
    return deduped

def cross_reference_findings(findings):
    # Example: secrets in Firebase config cross-referenced with Git
    for f in findings:
        if f.get('type') == 'EXPOSED_SECRET' and 'firebase' in f.get('resource',''):
            f['cross_reference'] = 'Secret also found in Firebase config.'
    return findings

def generate_dashboard_summary(findings):
    summary = {
        'total_findings': len(findings),
        'critical': sum(1 for f in findings if f.get('severity','').lower() == 'critical'),
        'high': sum(1 for f in findings if f.get('severity','').lower() == 'high'),
        'medium': sum(1 for f in findings if f.get('severity','').lower() == 'medium'),
        'low': sum(1 for f in findings if f.get('severity','').lower() == 'low'),
    }
    return summary

def export_sarif(findings):
    # Minimal SARIF v2.1.0 export for security tools
    sarif = {
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "DevSec Scanner"}},
            "results": [
                {
                    "ruleId": f.get('type',''),
                    "level": f.get('severity','').lower(),
                    "message": {"text": f.get('description','')},
                    "locations": [{"physicalLocation": {"artifactLocation": {"uri": f.get('resource','')}}}]
                } for f in findings
            ]
        }]
    }
    return json.dumps(sarif, indent=2)

def generate_consolidated_report(findings, ai_enabled=False, output_format='text'):
    findings = deduplicate_findings(findings)
    findings = cross_reference_findings(findings)
    summary = generate_dashboard_summary(findings)
    if output_format == 'sarif':
        return export_sarif(findings)
    if output_format == 'json':
        return json.dumps({'summary': summary, 'findings': findings}, indent=2)
    # Text format
    lines = ["EXECUTIVE DASHBOARD SUMMARY:"]
    for k,v in summary.items():
        lines.append(f"- {k}: {v}")
    lines.append("\nFINDINGS:")
    for f in findings:
        lines.append(f"[{f.get('severity','').upper()}] {f.get('type')}: {f.get('description','')} (Resource: {f.get('resource','')})")
        if f.get('cross_reference'):
            lines.append(f"  Cross-reference: {f['cross_reference']}")
    return '\n'.join(lines)

def test_consolidated_reporter():
    print("[TEST] Consolidated reporter...")
    findings = [
        {'type': 'EXPOSED_SECRET', 'severity': 'HIGH', 'description': 'Secret in repo', 'resource': 'git'},
        {'type': 'EXPOSED_SECRET', 'severity': 'HIGH', 'description': 'Secret in repo', 'resource': 'git'}
    ]
    out = generate_consolidated_report(findings, output_format='text')
    assert 'EXECUTIVE DASHBOARD SUMMARY' in out
    print("[PASS] Consolidated report generated.")
