"""
HTML report generation for DevSec Scanner
"""
import base64
import json
from src.devsec_scanner.reports.report_assets import REPORT_HTML_TEMPLATE, REPORT_CSS, REPORT_JS, CHART_JS_CDN

def render_findings_table(findings):
    rows = []
    for f in findings:
        ai_html = f'<button class="collapsible">AI</button><div class="collapsible-content">{f.get('ai_analysis','')}</div>' if f.get('ai_analysis') else ''
        rows.append(f"<tr class='severity-{f['severity'].upper()}'>"
                    f"<td>{f['severity'].capitalize()}</td>"
                    f"<td>{f['title']}</td>"
                    f"<td>{f['description']}</td>"
                    f"<td>{f.get('file_path','')}</td>"
                    f"<td>{f.get('remediation','')}</td>"
                    f"<td>{ai_html}</td>"
                    "</tr>")
    return '\n'.join(rows)

def render_summary(summary):
    return f"<b>Total Findings:</b> {summary['total_findings']}<br>" \
           f"<b>Security Score:</b> {summary['security_score']}<br>" \
           + ''.join([f"<b>{k.capitalize()}:</b> {v} " for k,v in summary['severity_breakdown'].items()])

def render_appendix(meta, config, stats):
    return f"<b>Scan Metadata:</b><br><pre>{json.dumps(meta, indent=2)}</pre>" \
           f"<b>Configuration:</b><br><pre>{json.dumps(config, indent=2)}</pre>" \
           f"<b>Stats:</b><br><pre>{json.dumps(stats, indent=2)}</pre>"

def build_html_report(report, config=None, stats=None):
    css_b64 = base64.b64encode(REPORT_CSS.encode()).decode()
    summary_html = render_summary(report['summary'])
    findings_html = render_findings_table(report['findings'])
    appendix_html = render_appendix(report['scan_metadata'], config or {}, stats or {})
    raw_json = json.dumps(report, indent=2)
    html = REPORT_HTML_TEMPLATE.format(
        css_b64=css_b64,
        chart_js=CHART_JS_CDN,
        css=REPORT_CSS,
        js=REPORT_JS,
        summary_html=summary_html,
        findings_html=findings_html,
        appendix_html=appendix_html,
        raw_json=raw_json
    )
    return html

def test_html_reporter():
    print("[TEST] HTML reporter...")
    report = {
        'summary': {'total_findings': 2, 'security_score': 80, 'severity_breakdown': {'critical':1,'high':1,'medium':0,'low':0}},
        'findings': [
            {'severity':'CRITICAL','title':'AWS Key','description':'Exposed','ai_analysis':'AI says bad.'},
            {'severity':'HIGH','title':'Open S3','description':'Public bucket','ai_analysis':''}
        ],
        'scan_metadata': {'scanner_version':'1.0.0'}
    }
    html = build_html_report(report)
    assert '<html' in html
    print("[PASS] HTML report generated.")

# HTML Reporter for scan results

class HTMLReporter:
    def report(self, results):
        # TODO: Output results as HTML
        pass
