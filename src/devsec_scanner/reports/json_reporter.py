"""
Structured JSON report generation for DevSec Scanner
"""
import uuid
import json
from src.devsec_scanner.reports.report_schema import validate_report_schema
from src.devsec_scanner.reports.report_metadata import get_scan_metadata

# JSON Reporter for scan results

class JSONReporter:
    def report(self, results):
        # TODO: Output results as JSON
        pass

def build_json_report(findings, target, scan_types, configuration, duration, summary=None):
    # Build summary if not provided
    if summary is None:
        sev_map = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for f in findings:
            sev = f.get("severity", "low").lower()
            if sev in sev_map:
                sev_map[sev] += 1
        summary = {
            "total_findings": len(findings),
            "severity_breakdown": sev_map,
            "security_score": max(0, 100 - sev_map["critical"]*20 - sev_map["high"]*10 - sev_map["medium"]*5)
        }
    # Structure findings
    structured = []
    for f in findings:
        structured.append({
            "id": f.get("id") or str(uuid.uuid4()),
            "scanner_type": f.get("scanner_type", "unknown"),
            "vulnerability_type": f.get("vulnerability_type", "unknown"),
            "severity": f.get("severity", "low"),
            "title": f.get("title", ""),
            "description": f.get("description", ""),
            "file_path": f.get("file_path", ""),
            "line_number": f.get("line_number"),
            "context": f.get("context", ""),
            "remediation": f.get("remediation", ""),
            "ai_analysis": f.get("ai_analysis", ""),
            "confidence": f.get("confidence", 80)
        })
    report = {
        "scan_metadata": get_scan_metadata(target, scan_types, configuration, duration),
        "summary": summary,
        "findings": structured
    }
    # Validate schema
    validate_report_schema(report)
    return json.dumps(report, indent=2)

def test_json_reporter():
    print("[TEST] JSON reporter...")
    findings = [{
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
    }]
    out = build_json_report(findings, "/tmp", ["git"], {}, 12.3)
    import json as js
    js.loads(out)  # Should not raise
    print("[PASS] JSON report generated and valid.")
