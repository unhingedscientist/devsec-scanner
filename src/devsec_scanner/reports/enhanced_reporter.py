"""
AI-integrated reporting system for enhanced vulnerability reports
"""
from src.devsec_scanner.ai.ai_risk_assessor import ai_risk_score
from src.devsec_scanner.ai.ai_explanations import get_ai_explanation

def generate_enhanced_report(findings, context, fmt='text'):
    """
    findings: list of dicts (from scanners)
    context: dict (env, compliance, business_criticality, etc)
    Returns: formatted report (text/JSON)
    """
    import json
    report = []
    for f in findings:
        risk = ai_risk_score(f, context)
        explanation = get_ai_explanation(f, context)
        entry = {
            'vulnerability': f['type'],
            'severity': f['severity'],
            'business_impact': risk['business_impact'],
            'explanation': explanation,
            'remediation': f.get('remediation', ''),
            'priority': risk['priority'],
            'risk_score': risk['risk_score'],
            'compliance': risk['compliance'],
            'effort': risk['effort'],
            'details': f.get('description', ''),
            'resource': f.get('resource', ''),
        }
        report.append(entry)
    if fmt == 'json':
        return json.dumps(report, indent=2)
    # Text format: executive summary, details, roadmap
    lines = ["EXECUTIVE SUMMARY:"]
    for r in report:
        lines.append(f"- {r['vulnerability']} (Priority {r['priority']}): {r['business_impact']}")
    lines.append("\nTECHNICAL DETAILS:")
    for r in report:
        lines.append(f"\nVULNERABILITY: {r['vulnerability']} ({r['severity']})")
        lines.append(f"BUSINESS IMPACT: {r['business_impact']}")
        lines.append(f"EXPLANATION: {r['explanation']}")
        lines.append(f"REMEDIATION: {r['remediation']}")
        lines.append(f"PRIORITY: {r['priority']} | RISK SCORE: {r['risk_score']}")
        lines.append(f"COMPLIANCE: {r['compliance']}")
        lines.append(f"EFFORT: {r['effort']}")
        lines.append(f"DETAILS: {r['details']}")
        lines.append(f"RESOURCE: {r['resource']}")
    lines.append("\nREMEDIATION ROADMAP:")
    for r in sorted(report, key=lambda x: x['priority']):
        lines.append(f"- [{r['priority']}] {r['vulnerability']}: {r['remediation']} (Effort: {r['effort']})")
    return '\n'.join(lines)

def test_enhanced_reporter():
    print("[TEST] Enhanced reporter...")
    findings = [
        {'type': 'PUBLIC_S3_BUCKET', 'severity': 'CRITICAL', 'remediation': 'Block public access', 'description': 'Bucket is public.'}
    ]
    context = {'env': 'prod', 'compliance': 'PCI-DSS', 'business_criticality': 'high'}
    out = generate_enhanced_report(findings, context)
    assert 'EXECUTIVE SUMMARY' in out
    print("[PASS] Enhanced report generated.")
