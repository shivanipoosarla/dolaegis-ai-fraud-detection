# Dashboard Prototype

DolAegis includes a static HTML dashboard generated from scored transaction results.

The dashboard is intentionally simple and self-contained. It does not require a frontend framework, database, login system, or hosted service. This keeps the portfolio version easy to run while still showing how fraud-scoring results could be presented to an SMB merchant or analyst.

## What the dashboard shows

- Total transactions analyzed
- Average risk score
- High-risk transaction count
- Manual-review queue size
- Approved transaction count
- Top recurring risk factors
- Transaction-level decision table
- Recommended action per transaction

## How to generate it

```bash
PYTHONPATH=src python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports
```

Open:

```text
reports/fraud_dashboard.html
```

## Why this matters

The original DolAegis strategy emphasizes real-time visibility, explainable decisions, merchant dashboards, alerts, and actionable recommendations for SMB users. This dashboard demonstrates that product direction without pretending the prototype is a full production SaaS platform.

## Current limitations

- Static HTML only
- No authentication or RBAC
- No live database
- No real-time refresh
- No merchant-specific tenant isolation
- No hosted frontend

A production version would separate merchant tenants, enforce identity and access controls, use a persisted transaction store, and update dashboard metrics from live scoring events.
