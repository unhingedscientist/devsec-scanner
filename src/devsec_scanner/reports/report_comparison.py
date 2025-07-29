"""
Before/after scan comparison logic for DevSec Scanner
"""
import difflib

def compare_reports(report_before, report_after):
    """
    Returns a dict with added, removed, and changed findings.
    """
    before_ids = {f['id']: f for f in report_before['findings']}
    after_ids = {f['id']: f for f in report_after['findings']}
    added = [after_ids[i] for i in after_ids if i not in before_ids]
    removed = [before_ids[i] for i in before_ids if i not in after_ids]
    changed = []
    for i in before_ids:
        if i in after_ids and before_ids[i] != after_ids[i]:
            changed.append({'before': before_ids[i], 'after': after_ids[i]})
    return {'added': added, 'removed': removed, 'changed': changed}

def test_report_comparison():
    print("[TEST] Report comparison...")
    before = {'findings':[{'id':'1','severity':'HIGH'}]}
    after = {'findings':[{'id':'1','severity':'CRITICAL'},{'id':'2','severity':'LOW'}]}
    diff = compare_reports(before, after)
    assert len(diff['added']) == 1 and len(diff['changed']) == 1
    print("[PASS] Report comparison works.")
