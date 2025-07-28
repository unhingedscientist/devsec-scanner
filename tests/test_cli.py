
import pytest
from click.testing import CliRunner
from src.devsec_scanner import cli
import os
import tempfile
import json
import sys
import types

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli.main, ['--help'])
    assert result.exit_code == 0
    assert "DevSec Scanner CLI" in result.output

def test_cli_version(runner):
    result = runner.invoke(cli.main, ['--version'])
    assert result.exit_code == 0
    assert "DevSec Scanner, version" in result.output


class DummyProgress:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def add_task(self, *a, **k):
        return 1
    def update(self, *a, **k):
        pass

def test_scan_firebase_success(runner, monkeypatch):
    monkeypatch.setattr("src.devsec_scanner.cli.Progress", DummyProgress)
    result = runner.invoke(cli.main, ['scan', 'firebase', 'dummy_path'])
    assert result.exit_code == 0
    assert "Firebase scan complete" in result.output

    monkeypatch.setattr("src.devsec_scanner.cli.Progress", DummyProgress)
    result = runner.invoke(cli.main, ['scan', 'git', 'dummy_path'])
    assert result.exit_code == 0
    assert "Git scan complete" in result.output

    monkeypatch.setattr("src.devsec_scanner.cli.Progress", DummyProgress)
    result = runner.invoke(cli.main, ['scan', 's3', 'dummy_bucket'])
    assert result.exit_code == 0
    assert "S3 scan complete" in result.output

    monkeypatch.setattr("src.devsec_scanner.cli.Progress", DummyProgress)
    result = runner.invoke(cli.main, ['scan', 'all', 'dummy_path'])
    assert result.exit_code == 0
    assert "All-platform scan complete" in result.output

def test_config_loading(monkeypatch, tmp_path):
    config_content = "OPENAI_API_KEY: test-key\nVERBOSE: true"
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    from src.devsec_scanner.config.settings import Config
    config = Config(config_path=str(config_file))
    assert config.OPENAI_API_KEY == "test-key"
    assert config.VERBOSE is True

def test_error_handling(monkeypatch, runner):
    # Simulate error in scan
    monkeypatch.setattr("src.devsec_scanner.cli.firebase", lambda ctx, path: (_ for _ in ()).throw(Exception("Simulated error")))
    result = runner.invoke(cli.main, ['scan', 'firebase', 'dummy_path'])
    assert result.exit_code != 0
    assert "ERROR" in result.output or "error" in result.output.lower()
