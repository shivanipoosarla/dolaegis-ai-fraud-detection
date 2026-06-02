# DolAegis: AI Fraud Detection SaaS Prototype

DolAegis is a portfolio prototype for SMB e-commerce fraud-risk scoring. It ingests synthetic transaction data, assigns explainable risk scores, exposes a small FastAPI scoring API, and generates Markdown, JSON, audit-log, and static HTML dashboard outputs for review workflows.

> Status: runnable prototype. The current implementation uses an explainable rules-based scoring engine. It does **not** claim to be a production ML fraud model, a certified fraud platform, or a live payment integration.

## Why this project exists

Small e-commerce merchants often need fraud triage without building a full enterprise fraud platform. DolAegis models a lightweight SaaS workflow:

```text
Transaction input -> Risk scoring -> Explanation -> Decision -> Report / Dashboard / Audit record
```

The product direction is based on an SMB-first SaaS strategy: real-time scoring, explainable decisions, API-first delivery, plug-and-play integrations, dashboard visibility, governance controls, and future integrations with platforms such as Shopify, WooCommerce, Stripe, and PayPal.

## What it demonstrates

- Python fraud-risk scoring engine
- FastAPI mock service for single and batch transaction scoring
- Explainable decision logic and human-review queue design
- Synthetic e-commerce transaction dataset
- Markdown, JSON, JSONL audit, and static HTML dashboard generation
- Governance-aware audit record with hashed user identifiers
- Documentation for SaaS architecture, API design, security, compliance, data governance, model risk, and threat modeling
- Unit tests and GitHub Actions workflow

## Quick start

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the CLI demo:

```bash
python -m compileall src tests
PYTHONPATH=src python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports
PYTHONPATH=src python -m unittest discover -s tests -v
```

Or use Make:

```bash
make check
make demo
```

Expected CLI output:

```text
Analyzed 6 transactions. High risk: 2. Manual review: 1. Approved: 3.
Reports, dashboard, and audit log written to: reports
```

Generated outputs:

```text
reports/fraud_risk_report.md
reports/fraud_risk_report.json
reports/fraud_dashboard.html
reports/audit_log.jsonl
```

Open the dashboard locally:

```text
reports/fraud_dashboard.html
```

## API demo

Run the API locally:

```bash
PYTHONPATH=src uvicorn dolaegis.api:app --reload
```

Open the interactive docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Score one transaction:

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d @api-examples/score_request.json
```

Batch score transactions:

```bash
curl -X POST http://127.0.0.1:8000/batch-score \
  -H "Content-Type: application/json" \
  -d @api-examples/batch_score_request.json
```

## Example risk factors

The current scoring engine evaluates explainable signals such as:

- High transaction amount
- Billing/shipping country mismatch
- IP/billing country mismatch
- New or young account
- Failed-login spike
- Transaction velocity spike
- New device
- Prior chargebacks
- High-risk country flag
- Unusual transaction hour

## Decisions

| Score | Risk level | Decision |
|---:|---|---|
| 0-39 | low | approve |
| 40-69 | medium | manual_review |
| 70-100 | high | block |

## Architecture

```text
CSV dataset                         API JSON request
    |                                      |
    v                                      v
CLI loader                         FastAPI endpoint
    |                                      |
    +---------------+----------------------+
                    |
                    v
             Transaction model
                    |
                    v
        Explainable risk engine
                    |
                    v
              RiskResult object
                    |
     +--------------+--------------+----------------+
     |              |              |                |
     v              v              v                v
Markdown/JSON   HTML dashboard   JSONL audit     API response
reports         preview          log             payload
```

## Project structure

```text
src/dolaegis/
  api.py              FastAPI API prototype
  cli.py              Command-line entry point
  dashboard.py        Static HTML dashboard generator
  governance.py       Audit-log and user-hash helpers
  models.py           Transaction data model
  reporting.py        Markdown/JSON report writers
  risk_engine.py      Explainable scoring logic

api-examples/          Example API request payloads
config/                Demo scoring-policy metadata
data/                  Synthetic sample transactions
reports/               Generated sample reports and dashboard
docs/                  Architecture, API, governance, and upload notes
tests/                 Unit tests
.github/workflows/     GitHub Actions test workflow
```

## Documentation

- [API spec](docs/API_SPEC.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Dashboard notes](docs/DASHBOARD.md)
- [Security and compliance notes](docs/SECURITY_COMPLIANCE.md)
- [Data governance](docs/DATA_GOVERNANCE.md)
- [Model risk management](docs/MODEL_RISK_MANAGEMENT.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Operating model](docs/OPERATING_MODEL.md)
- [Project status](docs/PROJECT_STATUS.md)
- [GitHub upload guide](docs/GITHUB_UPLOAD_GUIDE.md)
- [Resume and LinkedIn snippets](docs/RESUME_LINKEDIN_SNIPPETS.md)

## Scope and limitations

Implemented:

- CSV-based transaction ingestion
- REST-style API mock with `/health`, `/score`, and `/batch-score`
- Explainable rules-based fraud scoring
- Risk levels and decisions: approve, manual_review, block
- Markdown, JSON, static HTML dashboard, and JSONL audit outputs
- Synthetic data only
- Unit tests and GitHub Actions workflow

Not implemented:

- Live Shopify, WooCommerce, Stripe, PayPal, or banking integrations
- Real payment-card processing
- Production ML training pipeline
- Database persistence
- Hosted web dashboard with login/session state
- Authentication, RBAC, tenant isolation, or API-key enforcement
- PCI DSS, GDPR, CCPA, SOC 2, or ISO 27001 compliance implementation

## Resume-safe wording

```text
Built DolAegis, a Python/FastAPI fraud-risk scoring prototype for SMB e-commerce transactions that exposes scoring endpoints, generates explainable risk decisions, and creates Markdown, JSON, audit-log, and static dashboard outputs for analyst review workflows.
```

## License

MIT License.
