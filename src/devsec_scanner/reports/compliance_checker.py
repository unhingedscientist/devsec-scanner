"""
Compliance framework impact assessment for DevSec Scanner
"""
COMPLIANCE_PENALTIES = {
    'GDPR': {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 3, 'LOW': 1},
    'SOX': {'CRITICAL': 8, 'HIGH': 5, 'MEDIUM': 2, 'LOW': 1},
    'PCI-DSS': {'CRITICAL': 12, 'HIGH': 8, 'MEDIUM': 4, 'LOW': 2}
}

def compliance_impact(findings, compliance):
    penalty = 0
    if not compliance:
        return 0
    if isinstance(compliance, str):
        compliance = [compliance]
    for f in findings:
        sev = f.get('severity', 'LOW').upper()
        for c in compliance:
            c = c.upper()
            if c in COMPLIANCE_PENALTIES:
                penalty += COMPLIANCE_PENALTIES[c][sev]
    return penalty

def test_compliance_checker():
    print("[TEST] Compliance checker...")
    findings = [{'severity': 'CRITICAL'}, {'severity': 'HIGH'}]
    penalty = compliance_impact(findings, ['GDPR', 'PCI-DSS'])
    assert penalty > 0
    print("[PASS] Compliance penalty:", penalty)
