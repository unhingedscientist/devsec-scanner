#!/usr/bin/env python3
import re
import sys
from pathlib import Path

version_file = Path('pyproject.toml')
if not version_file.exists():
    print('[ERROR] pyproject.toml not found')
    sys.exit(1)

content = version_file.read_text()
match = re.search(r'version\s*=\s*"([0-9]+)\.([0-9]+)\.([0-9]+)"', content)
if not match:
    print('[ERROR] Version not found in pyproject.toml')
    sys.exit(1)
major, minor, patch = map(int, match.groups())
patch += 1
new_version = f'{major}.{minor}.{patch}'
content = re.sub(r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', f'version = "{new_version}"', content)
version_file.write_text(content)
print(f'[INFO] Bumped version to {new_version}')
