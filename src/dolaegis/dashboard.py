from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Iterable, List

from .risk_engine import RiskResult


def summarize_results(results: Iterable[RiskResult]) -> dict[str, object]:
    """Return dashboard-level metrics for scored transactions."""
    result_list = list(results)
    count = len(result_list)
    level_counts = Counter(result.level for result in result_list)
    decision_counts = Counter(result.decision for result in result_list)
    factor_counts = Counter(
        factor.name for result in result_list for factor in result.factors
    )
    average_score = round(sum(result.score for result in result_list) / count, 2) if count else 0.0
    review_queue = [
        result for result in result_list if result.decision in {"block", "manual_review"}
    ]

    return {
        "transactions_analyzed": count,
        "average_score": average_score,
        "high_risk": level_counts.get("high", 0),
        "medium_risk": level_counts.get("medium", 0),
        "low_risk": level_counts.get("low", 0),
        "blocked": decision_counts.get("block", 0),
        "manual_review": decision_counts.get("manual_review", 0),
        "approved": decision_counts.get("approve", 0),
        "top_factors": factor_counts.most_common(5),
        "review_queue_size": len(review_queue),
    }


def _recommendation(result: RiskResult) -> str:
    if result.decision == "block":
        return "Block or hold order; verify identity/payment details before fulfillment."
    if result.decision == "manual_review":
        return "Route to manual review; inspect account history, device, and payment context."
    return "Approve automatically; continue passive monitoring."


def _badge(text: str) -> str:
    safe = escape(text)
    return f'<span class="badge badge-{safe}">{safe.replace("_", " ")}</span>'


def build_dashboard_html(results: List[RiskResult]) -> str:
    """Build a self-contained static HTML merchant dashboard.

    The dashboard is intentionally static so the portfolio demo works without a
    database, frontend build system, or hosted service.
    """
    summary = summarize_results(results)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    top_factor_items = "".join(
        f"<li><strong>{escape(name)}</strong>: {count} transaction(s)</li>"
        for name, count in summary["top_factors"]
    ) or "<li>No risk factors detected.</li>"

    table_rows = []
    for result in sorted(results, key=lambda item: item.score, reverse=True):
        factor_names = ", ".join(factor.name for factor in result.factors) or "none"
        table_rows.append(
            "<tr>"
            f"<td>{escape(result.transaction_id)}</td>"
            f"<td>{escape(result.user_id)}</td>"
            f"<td><strong>{result.score}</strong></td>"
            f"<td>{_badge(result.level)}</td>"
            f"<td>{_badge(result.decision)}</td>"
            f"<td>{escape(factor_names)}</td>"
            f"<td>{escape(_recommendation(result))}</td>"
            "</tr>"
        )

    rows_html = "\n".join(table_rows)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>DolAegis Fraud Risk Dashboard</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #111827;
      --muted: #94a3b8;
      --text: #e5e7eb;
      --line: #334155;
      --low: #16a34a;
      --medium: #ca8a04;
      --high: #dc2626;
      --review: #2563eb;
    }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 32px; }}
    header {{ margin-bottom: 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 34px; }}
    h2 {{ margin-top: 28px; }}
    .muted {{ color: var(--muted); }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; }}
    .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 18px; }}
    .card .value {{ font-size: 30px; font-weight: 700; margin-top: 6px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    @media (max-width: 800px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); border-radius: 14px; overflow: hidden; }}
    th, td {{ padding: 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: #cbd5e1; font-size: 13px; text-transform: uppercase; letter-spacing: .04em; }}
    .badge {{ display: inline-block; border-radius: 999px; padding: 3px 10px; font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    .badge-low, .badge-approve {{ background: rgba(22,163,74,.2); color: #86efac; }}
    .badge-medium, .badge-manual_review {{ background: rgba(202,138,4,.2); color: #fde68a; }}
    .badge-high, .badge-block {{ background: rgba(220,38,38,.2); color: #fecaca; }}
    .note {{ border-left: 4px solid var(--review); padding: 12px 16px; background: rgba(37,99,235,.12); }}
    code {{ color: #bfdbfe; }}
  </style>
</head>
<body>
  <main class="wrap">
    <header>
      <h1>DolAegis Fraud Risk Dashboard</h1>
      <p class="muted">Static merchant dashboard generated from synthetic transaction scoring results. Generated {generated_at}.</p>
      <p class="note">Prototype scope: explainable rules-based scoring for portfolio demonstration. This is not a production ML model, payment integration, or compliance-certified fraud system.</p>
    </header>

    <section class="cards" aria-label="Summary metrics">
      <div class="card"><div class="muted">Transactions</div><div class="value">{summary['transactions_analyzed']}</div></div>
      <div class="card"><div class="muted">Average Score</div><div class="value">{summary['average_score']}</div></div>
      <div class="card"><div class="muted">High Risk</div><div class="value">{summary['high_risk']}</div></div>
      <div class="card"><div class="muted">Manual Review</div><div class="value">{summary['manual_review']}</div></div>
      <div class="card"><div class="muted">Approved</div><div class="value">{summary['approved']}</div></div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Decision Queue</h2>
        <ul>
          <li><strong>{summary['blocked']}</strong> transaction(s) recommended for block/hold.</li>
          <li><strong>{summary['manual_review']}</strong> transaction(s) routed to manual review.</li>
          <li><strong>{summary['approved']}</strong> transaction(s) approved automatically.</li>
        </ul>
      </div>
      <div class="card">
        <h2>Top Risk Factors</h2>
        <ul>{top_factor_items}</ul>
      </div>
    </section>

    <section>
      <h2>Transaction Review Table</h2>
      <table>
        <thead>
          <tr>
            <th>Transaction</th>
            <th>User</th>
            <th>Score</th>
            <th>Risk</th>
            <th>Decision</th>
            <th>Factors</th>
            <th>Recommended Action</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </section>
  </main>
</body>
</html>
"""


def write_dashboard_html(results: List[RiskResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_dashboard_html(results), encoding="utf-8")
