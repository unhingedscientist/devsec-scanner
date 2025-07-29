# DevSec Scanner

DevSec Scanner is an AI-powered CLI tool that finds actually exploitable vulnerabilities in developer projects. Built by former bug bounty hunters, it provides actionable, contextual fix suggestions and a developer-first experience.

## 🚀 Value Proposition
- **Finds real, exploitable bugs** (not just noise)
- **AI-powered fix suggestions** for every finding
- **Fast, modular, and easy to use**
- **Supports Firebase, AWS S3, Git, APIs, Docker, MongoDB**

## 📦 Installation

### From PyPI (coming soon)
```sh
pip install devsec-scanner
```

### From Source
```sh
git clone https://github.com/yourusername/devsec-scanner.git
cd devsec-scanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ⚡ Quick Start

```sh
./scanner --help
./scanner all --ai-enabled --export results.json
./scanner firebase git --severity high
./scanner s3 --profile prod --ai-enabled
```

## 🔧 Configuration

You can use a `.scanner-config` YAML file to set global options:

```yaml
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
