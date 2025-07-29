"""
GitHub Actions workflow YAML generator for DevSec Scanner
"""
def generate_workflow_yaml():
    return '''name: Security Scanner
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'
  workflow_dispatch:
    inputs:
      scan_type:
        description: 'Scan type'
        required: true
        default: 'all'
        type: choice
        options: [all, firebase, git, s3]
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run Security Scanner
        run: |
          python main_scanner.py --ai-enabled --output-format json --severity-filter medium --export scan-results.json --parallel --timeout 600 --scanners ${{ github.event.inputs.scan_type || 'all' }}
      - name: Upload scan report artifact
        uses: actions/upload-artifact@v4
        with:
          name: devsec-scan-report
          path: scan-results.json
          retention-days: 14
      - name: Comment on PR with summary
        if: github.event_name == 'pull_request'
        run: |
          python src/devsec_scanner/github/pr_commenter.py --report scan-results.json --pr ${{ github.event.pull_request.number }}
      - name: Upload SARIF to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: scan-results.sarif
'''

def test_github_workflow():
    print("[TEST] GitHub workflow YAML generation...")
    yaml = generate_workflow_yaml()
    assert 'jobs:' in yaml
    print("[PASS] Workflow YAML generated.")
