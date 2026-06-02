# Data Governance and Lifecycle

The SaaS concept depends on transaction data, merchant profiles, device/session identifiers, fraud outcomes, and risk decisions. The presentation emphasizes standardized data intake, validation, storage, processing, archival, disposal, metadata catalogs, RBAC, audit trails, and data-quality scoring.

## Data lifecycle

```text
Transaction/API Input
  -> Validation and normalization
  -> Risk scoring
  -> Decision + explanation
  -> Report/dashboard output
  -> Audit record
  -> Retention and disposal policy
```

## Prototype data classes

| Data type | Example | Current handling |
|---|---|---|
| Transaction data | amount, countries, account age, velocity | Synthetic CSV and API payloads |
| User identifier | `user_id` | Hashed in audit records |
| Risk decision | approve/manual_review/block | Stored in reports |
| Risk explanation | factor names and text | Stored in reports/dashboard |
| Audit evidence | score, decision, factor names | JSONL audit output |

## Production governance backlog

- Define tenant isolation boundaries.
- Implement API authentication and RBAC.
- Encrypt all sensitive data at rest and in transit.
- Tokenize or avoid raw payment-card data.
- Define retention periods by data class.
- Add deletion/export workflows for privacy requests.
- Track data lineage from ingestion through decision output.
- Version scoring policies and model artifacts.
- Maintain an audit trail for manual decision overrides.
