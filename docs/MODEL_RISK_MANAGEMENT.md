# Model and Decision Risk Management

The current engine is rule-based. This is intentional for the portfolio version: it makes every decision explainable and avoids pretending that the project has a trained production fraud model.

## Current decision model

```text
Risk factors -> points -> score -> level -> decision
```

Decision thresholds:

| Score | Level | Decision |
|---:|---|---|
| 0-39 | low | approve |
| 40-69 | medium | manual_review |
| 70-100 | high | block |

## Why explainability matters

SMB users need to know why a transaction was flagged. The dashboard and reports expose risk factors such as new device, velocity spike, failed-login spike, country mismatch, and chargeback history.

## Production ML roadmap

A future ML version should include:

- Labeled fraud and chargeback outcome data.
- Train/validation/test splits.
- Precision, recall, F1, ROC-AUC, and false-positive-rate reporting.
- Drift monitoring.
- Human review feedback loop.
- Bias/fairness review for geography/device/account-age features.
- Model versioning and rollback.
- Champion/challenger evaluation.

## Human-in-the-loop controls

The prototype uses `manual_review` for medium-risk transactions. A production workflow should allow analysts or merchants to record whether they approved, blocked, refunded, or escalated the transaction, then feed confirmed outcomes back into future tuning.
