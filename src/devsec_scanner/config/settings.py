
import os
import yaml
import json
from dotenv import load_dotenv

class Config:
    # AI API Keys
    OPENAI_API_KEY: str = None
    ANTHROPIC_API_KEY: str = None

    # AWS Credentials
    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    AWS_DEFAULT_REGION: str = "us-east-1"

    # Firebase Credentials
    FIREBASE_SERVICE_ACCOUNT_PATH: str = None

    # Scanning Options
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    SCAN_TIMEOUT: int = 300  # 5 minutes
    AI_ENABLED: bool = True

    # Output Options
    OUTPUT_FORMAT: str = "console"  # console, json, html
    VERBOSE: bool = False

    def __init__(self, config_path=None, cli_overrides=None):
        # 1. Load .env
        load_dotenv()

        # 2. Load config file (YAML or JSON)
        file_config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                    file_config = yaml.safe_load(f) or {}
                elif config_path.endswith('.json'):
                    file_config = json.load(f)

        # 3. Load from environment variables
        env = os.environ

        # 4. CLI overrides
        cli = cli_overrides or {}

        # 5. Set values with priority: CLI > env > config file > default
        self.OPENAI_API_KEY = cli.get('OPENAI_API_KEY') or env.get('OPENAI_API_KEY') or file_config.get('OPENAI_API_KEY') or self.OPENAI_API_KEY
        self.ANTHROPIC_API_KEY = cli.get('ANTHROPIC_API_KEY') or env.get('ANTHROPIC_API_KEY') or file_config.get('ANTHROPIC_API_KEY') or self.ANTHROPIC_API_KEY
        self.AWS_ACCESS_KEY_ID = cli.get('AWS_ACCESS_KEY_ID') or env.get('AWS_ACCESS_KEY_ID') or file_config.get('AWS_ACCESS_KEY_ID') or self.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = cli.get('AWS_SECRET_ACCESS_KEY') or env.get('AWS_SECRET_ACCESS_KEY') or file_config.get('AWS_SECRET_ACCESS_KEY') or self.AWS_SECRET_ACCESS_KEY
        self.AWS_DEFAULT_REGION = cli.get('AWS_DEFAULT_REGION') or env.get('AWS_DEFAULT_REGION') or file_config.get('AWS_DEFAULT_REGION') or self.AWS_DEFAULT_REGION
        self.FIREBASE_SERVICE_ACCOUNT_PATH = cli.get('FIREBASE_SERVICE_ACCOUNT_PATH') or env.get('FIREBASE_SERVICE_ACCOUNT_PATH') or file_config.get('FIREBASE_SERVICE_ACCOUNT_PATH') or self.FIREBASE_SERVICE_ACCOUNT_PATH
        self.MAX_FILE_SIZE = int(cli.get('MAX_FILE_SIZE') or env.get('MAX_FILE_SIZE') or file_config.get('MAX_FILE_SIZE') or self.MAX_FILE_SIZE)
        self.SCAN_TIMEOUT = int(cli.get('SCAN_TIMEOUT') or env.get('SCAN_TIMEOUT') or file_config.get('SCAN_TIMEOUT') or self.SCAN_TIMEOUT)
        self.AI_ENABLED = self._parse_bool(cli.get('AI_ENABLED') or env.get('AI_ENABLED') or file_config.get('AI_ENABLED'), self.AI_ENABLED)
        self.OUTPUT_FORMAT = cli.get('OUTPUT_FORMAT') or env.get('OUTPUT_FORMAT') or file_config.get('OUTPUT_FORMAT') or self.OUTPUT_FORMAT
        self.VERBOSE = self._parse_bool(cli.get('VERBOSE') or env.get('VERBOSE') or file_config.get('VERBOSE'), self.VERBOSE)

        self._validate()

    def _parse_bool(self, value, default):
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("1", "true", "yes", "on")

    def _validate(self):
        missing = []
        if not self.OPENAI_API_KEY and not self.ANTHROPIC_API_KEY and self.AI_ENABLED:
            missing.append("OPENAI_API_KEY or ANTHROPIC_API_KEY (for AI features)")
        if not self.AWS_ACCESS_KEY_ID or not self.AWS_SECRET_ACCESS_KEY:
            missing.append("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (for AWS scanning)")
        if missing:
            print("[Config] Warning: Missing required settings: " + ", ".join(missing))
