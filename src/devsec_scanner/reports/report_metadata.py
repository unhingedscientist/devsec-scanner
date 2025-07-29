"""
Metadata collection and timestamp handling for scan reports
"""
import datetime
import platform
import getpass

def get_scan_metadata(target, scan_types, configuration, duration):
    return {
        "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
        "scanner_version": "1.0.0",
        "scan_duration": duration,
        "target": target,
        "scan_types": scan_types,
        "configuration": configuration,
        "host": platform.node(),
        "user": getpass.getuser()
    }

def test_report_metadata():
    print("[TEST] Report metadata...")
    meta = get_scan_metadata("/tmp", ["git"], {}, 12.3)
    assert meta["timestamp"].endswith('Z')
    assert meta["scanner_version"] == "1.0.0"
    print("[PASS] Metadata collection works.")
