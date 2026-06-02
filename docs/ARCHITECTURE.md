# Architecture

DolAegis is organized as a small, testable Python prototype with both CLI and API entry points.

```text
Synthetic transaction CSV              API JSON request
        |                                      |
        v                                      v
CLI transaction loader              FastAPI /score endpoint
        |                                      |
        +--------------+-----------------------+
                       |
                       v
             Transaction normalizer
                       |
                       v
          Explainable risk scoring engine
                       |
                       v
                 RiskResult objects
                       |
      +----------------+----------------+
      |                                 |
      v                                 v
Markdown/JSON reports             API JSON response
```

## SaaS concept

A production SaaS version would replace synthetic CSV/API payloads with authenticated ingestion from e-commerce and payment platforms. Scored events would feed merchant dashboards, review queues, notification systems, and compliance/audit logs.

## Current design choice

The current implementation is rule-based, not ML-based. This makes decisions explainable and easy to test. A later version could add a trained model score while preserving the explanation layer and API response contract.


## Dashboard Layer

The static dashboard generator converts scored results into an HTML risk-review view. It shows summary cards, decision queue counts, top risk factors, transaction-level decisions, and recommended actions. This mirrors the merchant-dashboard direction from the DolAegis product strategy while keeping the prototype easy to run locally.


## Governance layer added in Step 4

```text
Transaction Input
  -> Validation / normalization
  -> FraudRiskEngine
  -> RiskResult
  -> Report writers + Dashboard
  -> Governance audit record
```

The governance helper hashes user identifiers and records decision evidence in JSONL format. This demonstrates auditability and data-minimization thinking without storing real customer or payment data.
