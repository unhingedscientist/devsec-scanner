"""
firebase_detector.py
Detects Firebase projects and parses firebase.json, .firebaserc, and rules files.
"""
import os
import json
from typing import Dict, Any, Optional

class FirebaseDetectionError(Exception):
    pass

def detect_firebase_project(path: str) -> Dict[str, Any]:
    """
    Detects Firebase project files and parses firebase.json, .firebaserc, and rules files.
    Args:
        path: Directory path to scan
    Returns:
        Dictionary with project config and parsed rules structure
    Raises:
        FirebaseDetectionError: On invalid JSON, missing files, or permission errors
    """
    result = {
        "firebase_json": None,
        ".firebaserc": None,
        "firestore_rules": None,
        "storage_rules": None,
        "errors": []
    }
    # Detect firebase.json
    firebase_json_path = os.path.join(path, "firebase.json")
    firebaserc_path = os.path.join(path, ".firebaserc")
    firestore_rules_path = os.path.join(path, "firestore.rules")
    storage_rules_path = os.path.join(path, "storage.rules")

    # Parse firebase.json
    if os.path.exists(firebase_json_path):
        try:
            with open(firebase_json_path, "r") as f:
                result["firebase_json"] = json.load(f)
        except Exception as e:
            result["errors"].append(f"firebase.json: {e}")
    # Parse .firebaserc
    if os.path.exists(firebaserc_path):
        try:
            with open(firebaserc_path, "r") as f:
                result[".firebaserc"] = json.load(f)
        except Exception as e:
            result["errors"].append(f".firebaserc: {e}")
    # Read rules files (raw text)
    if os.path.exists(firestore_rules_path):
        try:
            with open(firestore_rules_path, "r") as f:
                result["firestore_rules"] = f.read()
        except Exception as e:
            result["errors"].append(f"firestore.rules: {e}")
    if os.path.exists(storage_rules_path):
        try:
            with open(storage_rules_path, "r") as f:
                result["storage_rules"] = f.read()
        except Exception as e:
            result["errors"].append(f"storage.rules: {e}")
    if not result["firebase_json"] and not result[".firebaserc"]:
        raise FirebaseDetectionError("No Firebase project files found in directory.")
    return result

# --- Test function ---
def _test_detect_firebase_project():
    import tempfile, shutil
    tempdir = tempfile.mkdtemp()
    try:
        with open(os.path.join(tempdir, "firebase.json"), "w") as f:
            f.write('{"hosting": {}}')
        with open(os.path.join(tempdir, ".firebaserc"), "w") as f:
            f.write('{"projects": {"default": "demo"}}')
        with open(os.path.join(tempdir, "firestore.rules"), "w") as f:
            f.write("rules_version = '2';\nservice cloud.firestore {\nmatch /databases/{database}/documents {}}")
        result = detect_firebase_project(tempdir)
        assert result["firebase_json"] is not None
        assert result[".firebaserc"] is not None
        assert result["firestore_rules"] is not None
        print("[test] firebase_detector.py: PASS")
    finally:
        shutil.rmtree(tempdir)

if __name__ == "__main__":
    _test_detect_firebase_project()
