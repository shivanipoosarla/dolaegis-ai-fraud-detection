# Project Status

DolAegis is GitHub-ready as a portfolio prototype.

## Implemented

- Synthetic e-commerce transaction dataset.
- Transaction normalization.
- Explainable rules-based fraud-risk scoring.
- Risk classification and decision logic.
- CLI batch scoring from CSV.
- FastAPI mock service with `/health`, `/score`, and `/batch-score`.
- Markdown and JSON report generation.
- Static HTML dashboard generation.
- Privacy-aware JSONL audit-log generation.
- Demo scoring-policy metadata in `config/risk_policy.json`.
- Unit tests.
- GitHub Actions workflow.
- Documentation for API design, architecture, dashboard, data governance, security/compliance, model risk, threat modeling, and operating model.

## Not implemented

- Real payment processor integrations.
- Real Shopify, WooCommerce, Stripe, PayPal, or banking APIs.
- Production ML training pipeline.
- Database persistence.
- Hosted web dashboard with authentication.
- Production authentication, API keys, OAuth, RBAC, or tenant isolation.
- Production audit-log storage.
- PCI DSS, GDPR, CCPA, SOC 2, ISO 27001, or any other formal compliance certification.

## Why the current model is rules-based

The current version intentionally uses an explainable rules-based engine. That makes the prototype easy to run, inspect, and test. It also avoids overclaiming an ML model without real labeled fraud data, evaluation metrics, monitoring, drift controls, or production governance.

## Reasonable future improvements

- Add configurable rule weights from `config/risk_policy.json`.
- Add a synthetic ML experiment with clear train/test metrics.
- Add a small persisted SQLite demo for scored transactions.
- Add simulated Shopify/Stripe-style adapter payloads.
- Add API-key middleware for local demo authentication.
- Add Dockerfile and hosted-demo instructions.
