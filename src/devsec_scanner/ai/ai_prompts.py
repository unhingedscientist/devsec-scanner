"""
Structured prompt templates for AI vulnerability explanations and fix suggestions
"""
PROMPT_TEMPLATES = {
    'firebase_public_rules': (
        "Explain the security risk of Firebase rules allowing public access. "
        "Rules: {rules}. Provide remediation steps and business impact."
    ),
    'firebase_missing_auth': (
        "Explain the risk of missing authentication in Firebase rules. "
        "Rules: {rules}. Suggest fixes and business impact."
    ),
    'git_exposed_api_key': (
        "Explain the risk of an exposed API key in Git. Key context: {context}. "
        "Provide remediation and business risk."
    ),
    'git_exposed_db_cred': (
        "Explain the risk of exposed database credentials in Git. Context: {context}. "
        "Provide remediation and business risk."
    ),
    's3_public_bucket': (
        "Explain the security implications of an AWS S3 bucket with public read access containing {file_types}. "
        "Provide specific remediation steps and business risk assessment."
    ),
    's3_encryption_issue': (
        "Explain the risk of an S3 bucket without default encryption. Bucket: {bucket}. "
        "Provide remediation and business impact."
    ),
    'general_security': (
        "Explain the security context and business impact of the following vulnerability: {description}. "
        "Provide actionable remediation steps."
    ),
}

def get_prompt(template_key, **kwargs):
    template = PROMPT_TEMPLATES.get(template_key, PROMPT_TEMPLATES['general_security'])
    return template.format(**kwargs)

def test_ai_prompts():
    print("[TEST] AI prompt templates...")
    prompt = get_prompt('s3_public_bucket', file_types='images, documents')
    assert 'public read access' in prompt
    print("[PASS] AI prompt for S3 public bucket generated.")
