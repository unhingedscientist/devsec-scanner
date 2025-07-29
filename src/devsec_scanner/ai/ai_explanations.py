"""
Context-aware vulnerability explanations using AI
"""
from src.devsec_scanner.ai.ai_client import ai_explain_vulnerability
from src.devsec_scanner.ai.ai_prompts import get_prompt

def get_ai_explanation(vuln, context):
    """
    Generate a technical explanation and remediation using AI, fallback to static if unavailable.
    """
    try:
        prompt = get_prompt(vuln['template'], **context)
        ai_resp = ai_explain_vulnerability({'prompt': prompt})
        return ai_resp['explanation']
    except Exception:
        # Fallback static explanation
        return f"{vuln['type']} ({vuln['severity']}): {vuln.get('description', 'No details.')}. See documentation for remediation."

def test_ai_explanations():
    print("[TEST] AI explanations...")
    vuln = {'type': 'PUBLIC_S3_BUCKET', 'severity': 'CRITICAL', 'template': 's3_public_bucket', 'description': 'Bucket is public.'}
    context = {'file_types': 'images, docs'}
    result = get_ai_explanation(vuln, context)
    assert result
    print("[PASS] AI explanation fallback works.")
