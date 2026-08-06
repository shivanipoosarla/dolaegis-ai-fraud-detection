# Architecture

DolAegis is a Python application with two entry points:

- A command-line interface for processing transaction data from a CSV file
- A FastAPI service for scoring transactions submitted as JSON

Both entry points use the same transaction model and risk-scoring engine.

## Components

### Transaction model

`models.py` defines the normalized transaction structure used by the scoring engine.

For CSV input, it converts text values into the expected Python types and normalizes country codes to uppercase.

### Risk-scoring engine

`risk_engine.py` evaluates each transaction using deterministic rules.

Each triggered rule produces a risk factor containing:

- A factor name
- A point value
- An explanation

The engine combines the points into a score from 0 to 100 and assigns one of three decisions:

- `approve`
- `manual_review`
- `block`

### Command-line interface

`cli.py` reads transactions from a CSV file, sends each transaction to the scoring engine, and writes the generated outputs to the selected reports directory.

The CLI produces:

- A JSON report
- A Markdown report
- A static HTML dashboard
- A JSONL audit log

### API service

`api.py` exposes the scoring engine through FastAPI.

The service provides:

- `GET /health`
- `POST /score`
- `POST /batch-score`

Pydantic models validate API request fields before transactions are sent to the scoring engine.

## API Data Flow

```text
JSON request
    |
    v
FastAPI endpoint
    |
    v
Pydantic request validation
    |
    v
Transaction model conversion
    |
    v
FraudRiskEngine
    |
    +------------------+
    |                  |
    v                  v
Risk result      Audit record
    |                  |
    +---------+--------+
              |
              v
        JSON response
```

### Report generation

`reporting.py` converts scoring results into JSON and Markdown reports.

### Dashboard generation

`dashboard.py` summarizes scoring results and generates a self-contained HTML dashboard.

The dashboard includes:

- Transaction counts
- Average risk score
- Decision totals
- Common risk factors
- Transaction-level results
- Recommended review actions

### Audit-record generation

`governance.py` generates a structured audit record for each scoring decision.

The record contains:

- The transaction identifier
- A hashed user identifier
- The risk score and decision
- The triggered risk-factor names
- A reduced summary of the transaction inputs

The audit records are written in JSONL format by the command-line workflow and returned as JSON by the API.

## CLI Data Flow

```text
CSV file
    |
    v
CSV loader and transaction normalization
    |
    v
FraudRiskEngine
    |
    v
RiskResult objects
    |
    +-------------------+-------------------+------------------+
    |                   |                   |                  |
    v                   v                   v                  v
JSON report       Markdown report     HTML dashboard     JSONL audit log
```
