# DevSec Scanner Configuration

## scanner-config.yml Example

```yaml
reporting:
  formats: [json, html, pdf]
  include_ai_analysis: true
  security_score: true

github:
  app_id: 123456
  private_key_path: /secrets/github-app.pem
  webhook_secret: ${WEBHOOK_SECRET}

scanning:
  default_severity: medium
  parallel_scans: true
  timeout: 300
```

## Environment Variables
- SCANNER_CONFIG: Path to config file
- GITHUB_APP_ID, GITHUB_PRIVATE_KEY_PATH, WEBHOOK_SECRET: GitHub App credentials
