"""
firebase_rules_parser.py
Parses Firebase security rules into a structured AST-like format.
"""
import re
from typing import List, Dict, Any, Optional

class FirebaseRulesParseError(Exception):
    pass

def parse_firebase_rules(rules_text: str) -> Dict[str, Any]:
    """
    Parses Firestore/Storage rules and extracts allow/match statements and conditions.
    Args:
        rules_text: The raw rules file content
    Returns:
        AST-like dictionary structure of rules
    Raises:
        FirebaseRulesParseError: On malformed rules syntax
    """
    ast = {"service": None, "matches": []}
    try:
        # Extract service
        service_match = re.search(r"service\s+(\w+)\s*{", rules_text)
        if service_match:
            ast["service"] = service_match.group(1)
        # Find all match blocks
        match_blocks = list(re.finditer(r"match\s+([^\s{]+)\s*{([^}]*)}", rules_text, re.DOTALL))
        for m in match_blocks:
            path = m.group(1)
            body = m.group(2)
            allows = []
            # Find all allow statements in this match block
            for allow in re.finditer(r"allow\s+([\w, ]+):\s*if\s*([^;]+);", body):
                actions = [a.strip() for a in allow.group(1).split(",")]
                condition = allow.group(2).strip()
                allows.append({"actions": actions, "condition": condition})
            ast["matches"].append({"path": path, "allows": allows})
        return ast
    except Exception as e:
        raise FirebaseRulesParseError(f"Malformed rules syntax: {e}")

# --- Test function ---
def _test_parse_firebase_rules():
    sample = """
    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        match /users/{userId} {
          allow read, write: if request.auth != null && request.auth.uid == userId;
        }
        match /public/{document} {
          allow read: if true;
          allow write: if request.auth != null;
        }
      }
    }
    """
    ast = parse_firebase_rules(sample)
    assert ast["service"] == "cloud.firestore"
    assert len(ast["matches"]) > 0
    print("[test] firebase_rules_parser.py: PASS")

if __name__ == "__main__":
    _test_parse_firebase_rules()
