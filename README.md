# Affy Scout & SecureML Core

Affy Scout is an AI-powered autonomous security platform with a modular, production-grade architecture:

- **affy_scout/**: CLI reconnaissance agent for scanning and data collection
- **secureml_core/**: AI orchestration engine for attack path modeling, autonomous fixes, and human-in-the-loop workflows
- **affy_dashboard/**: UI layer for visualization and management (placeholder)

## Key Features
- Modular scanner architecture (Firebase, Git secrets, S3, extensible)
- AI-powered attack chain analysis, fix suggestions, and auto-fix engine
- Dry-run, rollback, and approval workflows for safe autonomous actions
- Webhook, CI/CD, Slack/Discord, and audit trail integrations
- Test repo with known vulnerabilities for validation

## Quick Start

```sh
# Install dependencies
pip install -r requirements.txt

# Run a reconnaissance scan
python -m affy_scout.cli scout --target tests/test_repo --scanners firebase,git,s3 --output results.json

# Orchestrate findings and (optionally) auto-fix
python -m secureml_core.cli.secureml_cli orchestrate results.json --repo /path/to/repo --auto-fix --dry-run

# Run the webhook server for real-time events
python -m secureml_core.integrations.webhooks
```

## Usage Examples


### 1. Scan a local repo for secrets and misconfigurations
```sh
# Scan with all default scanners
python -m affy_scout.cli scout --target /path/to/repo --output scan.json

# Scan with specific scanners and custom output format
python -m affy_scout.cli scout --target /path/to/repo --scanners git,s3 --output scan.sarif --format sarif

# Scan a remote GitHub repo (clone and scan)
python -m affy_scout.cli scout --target https://github.com/example/repo --scanners git --output remote_scan.json
```

### 2. Analyze findings and suggest fixes (AI-powered)
```sh
# Analyze and get fix suggestions (dry-run, no changes made)
python -m secureml_core.cli.secureml_cli orchestrate scan.json --repo /path/to/repo --auto-fix --dry-run

# Analyze and create a pull request with fixes (requires approval)
python -m secureml_core.cli.secureml_cli orchestrate scan.json --repo /path/to/repo --auto-fix --approve

# Only generate a report, no fixes
python -m secureml_core.cli.secureml_cli orchestrate scan.json --repo /path/to/repo --report-only
```

### 3. Export and integrate results
```sh
# Export to SARIF for GitHub Advanced Security
python -m affy_scout.cli scout --target /path/to/repo --scanners git --output results.sarif --format sarif

# Export to CSV for compliance teams
python -m affy_scout.cli scout --target /path/to/repo --output results.csv --format csv
```

### 4. Real-time event handling and notifications
```sh
# Start webhook server (for CI/CD, Slack, etc.)
python -m secureml_core.integrations.webhooks

# Send notifications to Slack/Discord (configured in YAML)
# (No CLI command needed; handled by integration config)
```

### 5. Validate fixes using the test repo
```sh
# Scan and validate auto-fix on known vulnerable repo
python -m affy_scout.cli scout --target tests/test_repo --scanners firebase,git,s3 --output test_results.json
python -m secureml_core.cli.secureml_cli orchestrate test_results.json --repo tests/test_repo --auto-fix --dry-run
```

### 6. Advanced: Custom config and parallel scanning
```sh
# Use a custom config file
python -m affy_scout.cli scout --target /path/to/repo --config myscanner.yml --output custom.json

# Run multiple scans in parallel (default behavior, can be tuned in config)
python -m affy_scout.cli scout --target /repos/ --scanners git,s3 --parallel --output multi_scan.json
```

## Advanced Scenarios

### 1. Integrate with CI/CD Pipeline (GitHub Actions)
Add the following step to your `.github/workflows/security.yml`:
```yaml
  - name: Affy Scout Security Scan
    run: |
      pip install -r requirements.txt
      python -m affy_scout.cli scout --target ${{ github.workspace }} --output results.json
      python -m secureml_core.cli.secureml_cli orchestrate results.json --repo ${{ github.workspace }} --auto-fix --dry-run
```

### 2. Custom Scanner Plugin
Create `affy_scout/scanners/my_custom_scanner.py`:
```python
from affy_scout.scanners.base_scanner import BaseScanner

class MyCustomScanner(BaseScanner):
    name = "custom"
    def scan(self, target, config):
        # Custom logic here
        return [{"type": "custom_issue", "detail": "Example finding"}]
```
Register in your config or via CLI: `--scanners custom`

### 3. Slack/Discord Notification Integration
Edit your config YAML:
```yaml
integrations:
  slack:
    enabled: true
    webhook_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
  discord:
    enabled: true
    webhook_url: https://discord.com/api/webhooks/XXX/YYY
```

### 4. Automated Remediation Approval Workflow
Run in dry-run mode, review the plan, then approve:
```sh
python -m secureml_core.cli.secureml_cli orchestrate scan.json --repo /path/to/repo --auto-fix --dry-run
# Review output, then:
python -m secureml_core.cli.secureml_cli orchestrate scan.json --repo /path/to/repo --auto-fix --approve
```

### 5. Multi-Repo/Monorepo Scanning
```sh
find /repos/ -type d -name ".git" | xargs -n1 dirname | while read repo; do \
  python -m affy_scout.cli scout --target "$repo" --output "$repo-scan.json"; \
done
```

---

## Onboarding Guide


## Deep Dive Onboarding

### 1. Environment Setup
```sh
# Clone and enter the repo
git clone https://github.com/unhingedscientist/devsec-scanner.git
cd devsec-scanner

# (Recommended) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
- Copy or edit `affy_scout/config/scanner_config.py` for Python config, or create a YAML config (e.g. `myscanner.yml`).
- Set up API keys for AI providers (OpenAI, Claude) as environment variables or in config:
  - `export OPENAI_API_KEY=sk-...`
  - `export CLAUDE_API_KEY=...`
- (Optional) Configure Slack/Discord webhooks in your config YAML.

#### Example YAML config:
```yaml
scanners:
  - git
  - s3
output:
  format: json
  include_remediation: true
integrations:
  slack:
    enabled: true
    webhook_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
ai:
  enabled: true
  provider: openai
```

### 3. First Scan & Review
```sh
# Run a scan on your codebase
python -m affy_scout.cli scout --target /your/codebase --output results.json

# Pretty-print results (requires jq)
cat results.json | jq
```

### 4. AI-Powered Analysis & Fixes
```sh
# Dry-run (see suggestions, no changes made)
python -m secureml_core.cli.secureml_cli orchestrate results.json --repo /your/codebase --auto-fix --dry-run

# Approve and apply fixes (creates a PR or patch)
python -m secureml_core.cli.secureml_cli orchestrate results.json --repo /your/codebase --auto-fix --approve
```

### 5. Integration & Automation
- Add to CI/CD (see Advanced Scenarios)
- Enable notifications in config
- (Coming soon) Use the dashboard for visualization

### 6. Troubleshooting
- **Missing dependencies?** Run `pip install -r requirements.txt` again.
- **No findings?** Try scanning the included `tests/test_repo` for demo vulnerabilities.
- **AI not working?** Check your API key and provider config.
- **Need more help?** See `docs/USAGE.md` or open an issue on GitHub.

### 7. Next Steps
- Explore custom scanner plugins (see Advanced Scenarios)
- Integrate with your CI/CD pipeline
- Set up notifications and webhooks
- Review architecture in `docs/architecture.md`

For more, see `docs/USAGE.md` and `docs/architecture.md`.

---

## Workflow Diagram

```mermaid
flowchart TD
    A[Start: User/CI triggers scan] --> B[Affy Scout CLI: scout]
    B --> C[Scan Target(s) with Modular Scanners]
    C --> D[Output Results (JSON/SARIF/CSV)]
    D --> E[SecureML Core: orchestrate]
    E --> F[AI Analysis & Fix Suggestions]
    F --> G{Auto-fix?}
    G -- Yes, Dry-run --> H[Show Fix Plan, No Changes]
    G -- Yes, Approve --> I[Apply Fixes, Create PR]
    G -- No --> J[Report Only]
    H --> K[Audit Log & Notifications]
    I --> K
    J --> K
    K --> L[Export/Integrate: Webhooks, Slack, CI/CD]
    L --> M[Dashboard (optional)]
    M --> N[End]
```

## Safety & Oversight
- All autonomous actions support dry-run and rollback
- Approval required for critical changes (PR workflow)
- Full audit trail and change impact analysis

## Integration
- Webhooks for real-time events
- Slack/Discord notifications
- CI/CD pipeline hooks

## Testing & Validation
- Test repo with known vulnerabilities: `tests/test_repo/`
- Automated fix validation and regression testing

## Architecture
See `docs/architecture.md` for full details and diagrams.
ai:
  enabled: true
  provider: openai  # or claude
  max_requests_per_minute: 10
output:
  format: json
  include_remediation: true
  severity_filter: medium
scanning:
  parallel: true
  timeout: 300
```

## 🛡️ Supported Platforms
- Firebase
- AWS S3
- Git repositories
- APIs (coming soon)
- Docker (coming soon)
- MongoDB (coming soon)

## 📊 Reporting & Integration
- Consolidated reporting across all scan types
- Executive dashboard summary
- Export to JSON, text, or SARIF for CI/CD and security tools
- AI-powered explanations, risk scoring, and remediation

## 📝 Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License
MIT License. See [LICENSE](LICENSE) for details.
