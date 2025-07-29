# DevSec Scanner Usage

## CLI Examples

- Generate HTML report:
  ```sh
  ./scanner report --input scan-results.json --format html --output report.html
  ```
- GitHub setup:
  ```sh
  ./scanner github setup --repo owner/repo
  ```
- Scan a PR and comment:
  ```sh
  ./scanner github scan --repo owner/repo --pr 123
  ```
- Compare two scan reports:
  ```sh
  ./scanner compare --before scan1.json --after scan2.json --output diff.json
  ```

## Configuration Example

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
