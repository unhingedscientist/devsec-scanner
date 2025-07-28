
# Installation Guide

## Local Development

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/devsec-scanner.git
   cd devsec-scanner
   ```
2. Create a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your environment variables in `.env` or via export:
   ```env
   OPENAI_API_KEY=sk-...
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   ```

## CI/CD Integration

- Add `pip install -r requirements.txt` to your pipeline
- Set secrets as environment variables in your CI/CD provider
- Run CLI commands as part of your build/test steps

## Docker Installation (coming soon)

Docker support is planned for a future release.

## Troubleshooting

- **Missing API keys:** Ensure your `.env` or environment variables are set.
- **Dependency errors:** Run `pip install -r requirements.txt` again.
- **Permission errors:** Check file and directory permissions.
- **Other issues:** See [GitHub Issues](https://github.com/yourusername/devsec-scanner/issues) or open a new ticket.
