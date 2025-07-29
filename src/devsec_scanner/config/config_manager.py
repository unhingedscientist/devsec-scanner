"""
Configuration file handling for DevSec Scanner
"""
import os
import yaml

def load_config(path='.scanner-config'):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}

def test_config_manager():
    print("[TEST] Config manager...")
    import tempfile
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w')
    tmp.write('ai:\n  enabled: true\n')
    tmp.close()
    cfg = load_config(tmp.name)
    assert cfg['ai']['enabled'] is True
    print("[PASS] Config manager loads YAML.")
