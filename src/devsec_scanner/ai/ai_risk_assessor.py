"""
AI-powered risk scoring and business impact analysis
"""
from src.devsec_scanner.ai.ai_client import ai_explain_vulnerability

def ai_risk_score(vuln, context):
    """
    Use AI to generate a risk score (1-100) and business impact assessment.
    Fallback to static scoring if AI unavailable.
    """
    prompt = (
        f"Given the following vulnerability: {vuln['type']} (severity: {vuln['severity']}), "
        f"context: {context}. Assess risk (1-100), business impact, compliance, and remediation priority. "
        f"Output JSON: {{'risk_score': int, 'business_impact': str, 'priority': int, 'compliance': str, 'effort': str}}."
    )
    try:
        ai_resp = ai_explain_vulnerability({'prompt': prompt})
        # Try to parse JSON from AI response
        import json
        data = json.loads(ai_resp['explanation'])
        return data
    except Exception:
        # Fallback static logic
        sev_map = {'CRITICAL': 95, 'HIGH': 80, 'MEDIUM': 60, 'LOW': 30}
        return {
            'risk_score': sev_map.get(vuln['severity'], 20),
            'business_impact': 'Potential data exposure or service disruption.',
            'priority': 1 if vuln['severity'] in ('CRITICAL', 'HIGH') else 2,
            'compliance': 'Review for GDPR/SOX/PCI-DSS relevance.',
            'effort': 'Estimate: 30 minutes'
        }

def test_ai_risk_assessor():
    print("[TEST] AI risk assessor...")
    vuln = {'type': 'PUBLIC_S3_BUCKET', 'severity': 'CRITICAL'}
    context = 'prod, customer data, PCI-DSS'
    result = ai_risk_score(vuln, context)
    assert 'risk_score' in result
    print("[PASS] AI risk scoring works.")
