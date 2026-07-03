"""Generate a lightweight interactive workforce transformation dashboard HTML."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def generate_dashboard_html(data: dict[str, Any], output_file: Path) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data)
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Workforce AI Dashboard</title>
  <style>
    body {{ font-family: Segoe UI, Tahoma, sans-serif; margin: 0; padding: 16px; background: #f4f7fc; color: #13213a; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px; }}
    .card {{ background: #fff; border: 1px solid #d7e0ef; border-radius: 10px; padding: 12px; }}
    h1 {{ margin-top: 0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ border-bottom: 1px solid #e7ecf5; padding: 6px; text-align: left; }}
    .metric {{ font-size: 26px; font-weight: 700; color: #0d6f59; }}
    .meta {{ color: #5c6f8d; font-size: 12px; }}
    pre {{ background: #0f172a; color: #e2e8f0; padding: 8px; border-radius: 8px; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>Workforce AI Transformation Dashboard</h1>
  <p class=\"meta\">Decision support only. Human approval required for strategic actions.</p>
  <div class=\"grid\">
    <div class=\"card\"><h2>Anomalies</h2><div class=\"metric\" id=\"anomalyCount\"></div><table id=\"anomalyTable\"></table></div>
    <div class=\"card\"><h2>Opportunities</h2><div class=\"metric\" id=\"opportunityCount\"></div><table id=\"oppTable\"></table></div>
    <div class=\"card\"><h2>Readiness</h2><div class=\"metric\" id=\"readinessLevel\"></div><pre id=\"readinessJson\"></pre></div>
    <div class=\"card\"><h2>ROI Scenarios</h2><table id=\"roiTable\"></table></div>
    <div class=\"card\"><h2>KPI Targets</h2><table id=\"kpiTable\"></table></div>
  </div>
  <script>
    const DATA = {payload};
    const anomalies = DATA.anomalies || [];
    const opportunities = DATA.opportunities || [];
    const readiness = DATA.readiness || {{}};
    const roi = DATA.roi || [];
    const kpis = DATA.kpis || [];

    document.getElementById('anomalyCount').textContent = anomalies.length;
    document.getElementById('opportunityCount').textContent = opportunities.length;
    document.getElementById('readinessLevel').textContent = readiness.level || 'N/A';
    document.getElementById('readinessJson').textContent = JSON.stringify(readiness, null, 2);

    function fillTable(elId, headers, rows) {{
      const table = document.getElementById(elId);
      table.innerHTML = '';
      const thead = document.createElement('tr');
      headers.forEach(h => {{ const th = document.createElement('th'); th.textContent = h; thead.appendChild(th); }});
      table.appendChild(thead);
      rows.forEach(row => {{
        const tr = document.createElement('tr');
        row.forEach(cell => {{ const td = document.createElement('td'); td.textContent = cell; tr.appendChild(td); }});
        table.appendChild(tr);
      }});
    }}

    fillTable('anomalyTable', ['Type', 'Severity', 'Confidence'], anomalies.slice(0, 8).map(a => [a.anomaly_type, a.severity, a.confidence]));
    fillTable('oppTable', ['Task', 'Mode', 'Fit'], opportunities.slice(0, 8).map(o => [o.task_id, o.recommended_ai_mode, o.overall_ai_fit_score]));
    fillTable('roiTable', ['Scenario', 'Annual Savings', 'Payback Months'], roi.map(r => [r.scenario, r.annual_savings, r.payback_months]));
    fillTable('kpiTable', ['KPI', 'Target', 'Owner'], kpis.slice(0, 12).map(k => [k.name, `${{k.target_value}} ${{k.unit}}`, k.owner]));
  </script>
</body>
</html>
"""
    output_file.write_text(html, encoding="utf-8")
    return output_file
