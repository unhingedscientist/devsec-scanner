"""
whitelist_manager.py
Manages .secretsignore, inline ignores, and regex-based whitelisting.
"""
import os
import fnmatch
import re
from typing import List, Set, Pattern

class WhitelistManager:
    def __init__(self, root: str):
        self.patterns: Set[str] = set()
        self.regexes: List[Pattern] = []
        self.load_secretsignore(root)

    def load_secretsignore(self, root: str):
        path = os.path.join(root, '.secretsignore')
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('^') or line.endswith('$'):
                    try:
                        self.regexes.append(re.compile(line))
                    except Exception:
                        continue
                else:
                    self.patterns.add(line)

    def is_ignored(self, file_path: str, line: str = '', value: str = '') -> bool:
        # Path-based ignore
        for pat in self.patterns:
            if fnmatch.fnmatch(file_path, pat) or file_path.endswith(pat):
                return True
        # Inline ignore comments
        if '# secretsignore' in line or '// secretsignore' in line:
            return True
        # Regex ignore
        for regex in self.regexes:
            if regex.match(value):
                return True
        return False

# --- Test function ---
def _test_whitelist_manager():
    import tempfile, shutil
    tempdir = tempfile.mkdtemp()
    try:
        with open(os.path.join(tempdir, '.secretsignore'), 'w') as f:
            f.write('/tests/*\n*.test.js\nexample_api_key_*\n^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$\n')
        wm = WhitelistManager(tempdir)
        assert wm.is_ignored('tests/foo.py')
        assert wm.is_ignored('foo.test.js')
        assert wm.is_ignored('bar.py', value='example_api_key_123')
        assert wm.is_ignored('bar.py', value='550e8400-e29b-41d4-a716-446655440000')
        assert not wm.is_ignored('main.py', value='AKIAIOSFODNN7EXAMPLE')
        print('[test] whitelist_manager.py: PASS')
    finally:
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    _test_whitelist_manager()
