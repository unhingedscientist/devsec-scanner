"""
file_traversal.py
Recursive directory scanning with .gitignore support and file type filtering.
"""
import os
import fnmatch
from typing import List, Set, Iterator

GLOB_PATTERNS = ['*.env', '*.json', '*.py', '*.js', '*.yaml', '*.yml', '*.txt', '*.md']
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.exe', '.dll', '.so', '.zip', '.tar', '.gz', '.pdf', '.mp3', '.mp4', '.avi', '.mov', '.bin'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def load_gitignore(path: str) -> Set[str]:
    gitignore_path = os.path.join(path, '.gitignore')
    patterns = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.add(line)
    return patterns

def is_ignored(file_path: str, ignore_patterns: Set[str]) -> bool:
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path, pattern) or file_path.endswith(pattern):
            return True
    return False

def is_binary_file(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return True
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
    except Exception:
        return True
    return False

def scan_files(root: str) -> Iterator[str]:
    ignore_patterns = load_gitignore(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # Respect .gitignore for directories
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.relpath(os.path.join(dirpath, d), root), ignore_patterns)]
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(dirpath, filename), root)
            if is_ignored(rel_path, ignore_patterns):
                continue
            if not any(fnmatch.fnmatch(filename, pat) for pat in GLOB_PATTERNS):
                continue
            abs_path = os.path.join(dirpath, filename)
            if is_binary_file(abs_path):
                continue
            try:
                if os.path.getsize(abs_path) > MAX_FILE_SIZE:
                    continue
            except Exception:
                continue
            yield abs_path

# --- Test function ---
def _test_scan_files():
    import tempfile, shutil
    tempdir = tempfile.mkdtemp()
    try:
        with open(os.path.join(tempdir, 'test.env'), 'w') as f:
            f.write('AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE')
        with open(os.path.join(tempdir, 'test.py'), 'w') as f:
            f.write('api_key = "AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI"')
        with open(os.path.join(tempdir, '.gitignore'), 'w') as f:
            f.write('ignoreme.txt\n')
        with open(os.path.join(tempdir, 'ignoreme.txt'), 'w') as f:
            f.write('should not be found')
        files = list(scan_files(tempdir))
        assert any('test.env' in f for f in files)
        assert any('test.py' in f for f in files)
        assert not any('ignoreme.txt' in f for f in files)
        print('[test] file_traversal.py: PASS')
    finally:
        shutil.rmtree(tempdir)

if __name__ == '__main__':
    _test_scan_files()
