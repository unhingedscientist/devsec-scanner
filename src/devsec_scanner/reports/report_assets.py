"""
CSS, JavaScript, and HTML template management for reports
"""
CHART_JS_CDN = "https://cdn.jsdelivr.net/npm/chart.js"

REPORT_CSS = '''
body { font-family: 'Segoe UI', Arial, sans-serif; background: #f7f9fb; color: #222; margin: 0; }
.container { max-width: 1200px; margin: 2rem auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 2rem; }
h1, h2, h3 { color: #1a365d; }
.severity-CRITICAL { color: #fff; background: #d32f2f; }
.severity-HIGH { color: #fff; background: #f57c00; }
.severity-MEDIUM { color: #222; background: #ffd600; }
.severity-LOW { color: #fff; background: #388e3c; }
.theme-dark body { background: #181c24; color: #eee; }
.theme-dark .container { background: #232a36; }
.toggle-theme { float: right; cursor: pointer; }
@media (max-width: 700px) { .container { padding: 1rem; } }
.collapsible { cursor: pointer; }
.collapsible-content { display: none; padding: 0.5rem 1rem; }
.collapsible.active + .collapsible-content { display: block; }
input[type='search'] { padding: 0.5rem; margin: 0.5rem 0; width: 100%; border: 1px solid #ccc; border-radius: 4px; }
'''

REPORT_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" class="theme-light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevSec Scanner Report</title>
  <link rel="stylesheet" href="data:text/css;base64,{css_b64}">
  <script src="{chart_js}"></script>
  <style>{css}</style>
</head>
<body>
<div class="container">
  <h1>DevSec Scanner Report <span class="toggle-theme" onclick="toggleTheme()">🌓</span></h1>
  <div id="dashboard">
    <canvas id="scoreGauge" width="200" height="100"></canvas>
    <canvas id="severityPie" width="200" height="200"></canvas>
    <div id="metrics"></div>
  </div>
  <h2>Executive Summary</h2>
  <div id="summary">{summary_html}</div>
  <h2>Findings <input type="search" id="searchBox" placeholder="Search findings..."></h2>
  <table id="findingsTable">
    <thead><tr><th>Severity</th><th>Title</th><th>Description</th><th>File</th><th>Remediation</th><th>AI</th></tr></thead>
    <tbody>{findings_html}</tbody>
  </table>
  <h2>Technical Appendix</h2>
  <div id="appendix">{appendix_html}</div>
  <button onclick="toggleRawJson()">Show/Hide Raw JSON</button>
  <pre id="rawJson" style="display:none">{raw_json}</pre>
</div>
<script>{js}</script>
</body>
</html>
'''

REPORT_JS = '''
function toggleTheme() {
  var html = document.documentElement;
  html.classList.toggle('theme-dark');
  html.classList.toggle('theme-light');
}
document.querySelectorAll('.collapsible').forEach(function(btn) {
  btn.addEventListener('click', function() {
    this.classList.toggle('active');
    var content = this.nextElementSibling;
    if (content.style.display === 'block') content.style.display = 'none';
    else content.style.display = 'block';
  });
});
document.getElementById('searchBox').addEventListener('input', function() {
  var val = this.value.toLowerCase();
  document.querySelectorAll('#findingsTable tbody tr').forEach(function(row) {
    row.style.display = row.textContent.toLowerCase().includes(val) ? '' : 'none';
  });
});
function toggleRawJson() {
  var el = document.getElementById('rawJson');
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}
// Chart.js rendering
function renderCharts(score, sev) {
  new Chart(document.getElementById('scoreGauge'), {
    type: 'doughnut',
    data: { labels: ['Score', ''], datasets: [{ data: [score, 100-score], backgroundColor: ['#388e3c','#eee'] }] },
    options: { circumference: 180, rotation: 270, cutout: '80%', plugins: { legend: { display: false } } }
  });
  new Chart(document.getElementById('severityPie'), {
    type: 'pie',
    data: { labels: Object.keys(sev), datasets: [{ data: Object.values(sev), backgroundColor: ['#d32f2f','#f57c00','#ffd600','#388e3c'] }] },
    options: { plugins: { legend: { position: 'bottom' } } }
  });
}
// Call with data from backend
// renderCharts({score}, {sev_breakdown});
'''
