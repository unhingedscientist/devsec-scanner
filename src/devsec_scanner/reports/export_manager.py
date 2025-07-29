"""
Multi-format export coordination for DevSec Scanner reports
"""
import csv
import pdfkit
from src.devsec_scanner.reports.html_reporter import build_html_report

def export_html(report, path, config=None, stats=None):
    html = build_html_report(report, config, stats)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path

def export_pdf(report, path, config=None, stats=None):
    html = build_html_report(report, config, stats)
    pdfkit.from_string(html, path)
    return path

def export_csv(report, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=report['findings'][0].keys())
        writer.writeheader()
        for row in report['findings']:
            writer.writerow(row)
    return path
