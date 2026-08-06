# DolAegis: Explainable Fraud Risk Scoring

DolAegis is a Python application for evaluating synthetic e-commerce transactions using deterministic fraud-risk rules.

The project includes:

* A rules-based risk-scoring engine
* A FastAPI service for single and batch scoring
* A command-line interface
* Markdown and JSON reports
* A static HTML dashboard
* JSONL decision logs with hashed user identifiers
* Unit tests and a GitHub Actions workflow

This is an educational prototype. It does not process real payment data and should not be used as a production fraud-detection system.

## How It Works

Each transaction is evaluated against signals such as:

* High transaction amount
* Billing and shipping country mismatch
* IP and billing country mismatch
* New account activity
* Repeated failed logins
* Transaction velocity
* New device use
* Previous chargebacks
* High-risk country flag
* Unusual transaction time

Each triggered rule contributes to a score between 0 and 100.

| Score  | Risk level | Decision      |
| ------ | ---------- | ------------- |
| 0–39   | Low        | Approve       |
| 40–69  | Medium     | Manual review |
| 70–100 | High       | Block         |

The result includes the score, decision, risk level, and the rules that contributed to the decision.

## Project Structure

```text
src/dolaegis/
├── api.py          FastAPI endpoints
├── cli.py          Command-line interface
├── dashboard.py    Static dashboard generation
├── governance.py   Audit-log and identifier-hashing helpers
├── models.py       Transaction and result models
├── reporting.py    Markdown and JSON report generation
└── risk_engine.py  Fraud-risk scoring rules

api-examples/       Example API request payloads
config/             Scoring-policy metadata
data/               Synthetic transaction data
docs/               Technical documentation
reports/            Generated sample outputs
tests/              Unit tests
```

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/shivanipoosarla/dolaegis-ai-fraud-detection.git
cd dolaegis-ai-fraud-detection
python -m pip install -r requirements.txt
```

## Run the CLI

On macOS or Linux:

```bash
PYTHONPATH=src python -m dolaegis.cli \
  --input data/sample_transactions.csv \
  --outdir reports
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m dolaegis.cli --input data/sample_transactions.csv --outdir reports
```

The command generates:

```text
reports/fraud_risk_report.md
reports/fraud_risk_report.json
reports/fraud_dashboard.html
reports/audit_log.jsonl
```

## Run the API

On macOS or Linux:

```bash
PYTHONPATH=src uvicorn dolaegis.api:app --reload
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
uvicorn dolaegis.api:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Score One Transaction

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d @api-examples/score_request.json
```

### Score Multiple Transactions

```bash
curl -X POST http://127.0.0.1:8000/batch-score \
  -H "Content-Type: application/json" \
  -d @api-examples/batch_score_request.json
```

## Run the Tests

On macOS or Linux:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

You can also run:

```bash
make check
```

## Design Choices

The project uses deterministic rules rather than a trained machine-learning model because it does not include a sufficiently large labeled fraud dataset.

Rules make the current behavior:

* Reproducible
* Testable
* Explainable
* Suitable for demonstrating an end-to-end scoring workflow

The rule thresholds are demonstration values. They have not been calibrated against real transaction outcomes.

## Limitations

The current implementation does not include:

* Authentication or authorization
* Rate limiting
* Database persistence
* Tenant isolation
* Live payment-platform integrations
* A trained machine-learning model
* Production monitoring
* Regulatory or security certification

Some rules may create false positives. International purchases, new devices, and country mismatches can all occur during legitimate transactions.

## Documentation

* [Architecture](docs/ARCHITECTURE.md)
* [API specification](docs/API_SPEC.md)
* [Dashboard](docs/DASHBOARD.md)
* [Design decisions](docs/DESIGN_DECISIONS.md)
* [Security design](docs/SECURITY_DESIGN.md)

## License

MIT License
