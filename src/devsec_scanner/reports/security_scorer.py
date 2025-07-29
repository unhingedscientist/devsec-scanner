"""
Comprehensive security scoring algorithm for DevSec Scanner
"""
import datetime
from src.devsec_scanner.reports.severity_classifier import classify_severity
from src.devsec_scanner.reports.compliance_checker import compliance_impact

SEVERITY_WEIGHTS = {'CRITICAL': 10, 'HIGH': 7, 'MEDIUM': 4, 'LOW': 1}
ENV_MULTIPLIERS = {'prod': 2.0, 'production': 2.0, 'staging': 1.5, 'dev': 1.0, 'test': 1.0}


def calculate_security_score(findings, environment='prod', now=None, compliance=None):
    """
    Returns (score, breakdown, explanation)
    """
    base_score = 100
    now = now or datetime.datetime.utcnow()
    sev_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    deduction = 0
    age_penalty = 0
    ai_confidence_bonus = 0
    remediation_bonus = 0
    exposure_penalty = 0
    compliance_penalty = 0
    env_mult = ENV_MULTIPLIERS.get(environment, 1.0)
    for f in findings:
        sev = classify_severity(f)
        sev_counts[sev] += 1
        # Age-based penalty
        created = f.get('created_at')
        if created:
            try:
                created_dt = datetime.datetime.fromisoformat(created.replace('Z',''))
                age_days = (now - created_dt).days
                if age_days > 30:
                    age_penalty += 1 * env_mult
                if age_days > 90:
                    age_penalty += 2 * env_mult
            except Exception:
                pass
        # Exposure scope
        if f.get('exposure', '').lower() == 'public':
            exposure_penalty += 2 * env_mult
        # AI confidence
        conf = f.get('confidence', 80)
        if conf >= 95:
            ai_confidence_bonus += 0.5
        elif conf < 60:
            ai_confidence_bonus -= 1
    # Severity deductions
    for sev, count in sev_counts.items():
        deduction += SEVERITY_WEIGHTS[sev] * count * env_mult
    # Compliance penalty
    if compliance:
        compliance_penalty = compliance_impact(findings, compliance)
    # Remediation bonus
    if sev_counts['CRITICAL'] > 0 and all(f.get('remediation_difficulty','easy')=='easy' for f in findings if classify_severity(f)=='CRITICAL'):
        remediation_bonus = 5
    score = base_score - deduction - age_penalty - exposure_penalty - compliance_penalty + remediation_bonus + ai_confidence_bonus
    score = max(0, min(100, round(score)))
    explanation = {
        'base_score': base_score,
        'deduction': deduction,
        'age_penalty': age_penalty,
        'exposure_penalty': exposure_penalty,
        'compliance_penalty': compliance_penalty,
        'remediation_bonus': remediation_bonus,
        'ai_confidence_bonus': ai_confidence_bonus,
        'final_score': score,
        'environment_multiplier': env_mult,
        'severity_counts': sev_counts
    }
    return score, explanation

def test_security_scorer():
    print("[TEST] Security scorer...")
    findings = [
        {'severity': 'CRITICAL', 'created_at': '2025-06-01T00:00:00Z', 'exposure': 'public', 'confidence': 98, 'remediation_difficulty': 'easy'},
        {'severity': 'HIGH', 'created_at': '2025-07-01T00:00:00Z', 'exposure': 'internal', 'confidence': 80}
    ]
    score, expl = calculate_security_score(findings, environment='prod', compliance=['PCI-DSS'])
    assert 0 <= score <= 100
    print("[PASS] Security score:", score, expl)
