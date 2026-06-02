# Sample Report Preview

Run:

```bash
PYTHONPATH=src python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports
```

Generated files:

```text
reports/fraud_risk_report.md
reports/fraud_risk_report.json
```

The report lists each transaction, score, risk level, decision, and the exact factors that contributed to the score.


## Static Dashboard

The CLI also generates `reports/fraud_dashboard.html`, a self-contained HTML view with summary metrics, top risk factors, and transaction-level recommended actions.
