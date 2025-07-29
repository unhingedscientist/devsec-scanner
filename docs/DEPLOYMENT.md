# DevSec Scanner Deployment Guide

## CI/CD Integration
- Use `.github/workflows/security-scan.yml` for GitHub Actions
- Artifacts and SARIF upload supported

## Docker
- Multi-stage build for minimal image
- Non-root user for security
- Health checks enabled

## Local Development
- `docker-compose up --build`
- Mount scan targets and config as volumes

## Release Automation
- Use semantic versioning
- Tag releases and publish to PyPI/GitHub

## Security
- Scan your scanner with `devsecscanner` before release!
- Use secrets manager for credentials
