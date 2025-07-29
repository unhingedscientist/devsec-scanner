"""
JSON schema definition and validation for DevSec Scanner reports
"""
import jsonschema

SCAN_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "scan_metadata": {
            "type": "object",
            "properties": {
                "timestamp": {"type": "string", "format": "date-time"},
                "scanner_version": {"type": "string"},
                "scan_duration": {"type": "number"},
                "target": {"type": "string"},
                "scan_types": {"type": "array", "items": {"type": "string"}},
                "configuration": {"type": "object"}
            },
            "required": ["timestamp", "scanner_version", "scan_duration", "target", "scan_types", "configuration"]
        },
        "summary": {
            "type": "object",
            "properties": {
                "total_findings": {"type": "integer"},
                "severity_breakdown": {
                    "type": "object",
                    "properties": {
                        "critical": {"type": "integer"},
                        "high": {"type": "integer"},
                        "medium": {"type": "integer"},
                        "low": {"type": "integer"}
                    },
                    "required": ["critical", "high", "medium", "low"]
                },
                "security_score": {"type": "integer"}
            },
            "required": ["total_findings", "severity_breakdown", "security_score"]
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "scanner_type": {"type": "string"},
                    "vulnerability_type": {"type": "string"},
                    "severity": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "file_path": {"type": "string"},
                    "line_number": {"type": "integer"},
                    "context": {"type": "string"},
                    "remediation": {"type": "string"},
                    "ai_analysis": {"type": "string"},
                    "confidence": {"type": "integer"}
                },
                "required": ["id", "scanner_type", "vulnerability_type", "severity", "title", "description", "confidence"]
            }
        }
    },
    "required": ["scan_metadata", "summary", "findings"]
}

def validate_report_schema(report):
    try:
        jsonschema.validate(instance=report, schema=SCAN_REPORT_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        raise ValueError(f"Report schema validation error: {e}")

def test_report_schema():
    print("[TEST] Report schema validation...")
    sample = {
        "scan_metadata": {
            "timestamp": "2025-07-29T10:30:00Z",
            "scanner_version": "1.0.0",
            "scan_duration": 45.2,
            "target": "/path/to/scanned/directory",
            "scan_types": ["firebase", "git", "s3"],
            "configuration": {}
        },
        "summary": {
            "total_findings": 1,
            "severity_breakdown": {"critical": 1, "high": 0, "medium": 0, "low": 0},
            "security_score": 80
        },
        "findings": [
            {
                "id": "abc123",
                "scanner_type": "git",
                "vulnerability_type": "exposed_api_key",
                "severity": "critical",
                "title": "AWS Access Key Exposed",
                "description": "...",
                "file_path": "config/.env",
                "line_number": 15,
                "context": "...",
                "remediation": "...",
                "ai_analysis": "...",
                "confidence": 95
            }
        ]
    }
    assert validate_report_schema(sample)
    print("[PASS] Report schema validation works.")
