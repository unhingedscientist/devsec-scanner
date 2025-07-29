# DevSec Scanner Deployment

## Docker

- Build: `docker build -t devsecscanner .`
- Run: `docker run --rm -v $(pwd)/scan-targets:/scan-targets devsecscanner`

## Docker Compose

- `docker-compose up --build`

## Environment Variables
- SCANNER_CONFIG: Path to config file
- GITHUB_APP_ID, GITHUB_PRIVATE_KEY_PATH, WEBHOOK_SECRET: GitHub App credentials

## Health Check
- Service exposes port 8080 and health endpoint

## Production Tips
- Use a secrets manager for credentials
- Mount scan targets as read-only
- Monitor logs and health status
