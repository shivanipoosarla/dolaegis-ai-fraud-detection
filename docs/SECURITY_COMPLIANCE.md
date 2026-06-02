# Security and Compliance Notes

DolAegis is a portfolio prototype, not a certified fraud platform. This document shows how the product would need to be governed before handling real merchant or payment data.

## Compliance scope

The strategy presentation identifies PCI DSS, GDPR, CCPA, SOC 2-style controls, access governance, vulnerability scans, penetration tests, and audit trails as important design drivers for a fraud-detection SaaS handling merchant and transaction data.

In this repository:

- No real payment-card data is used.
- All sample data is synthetic.
- The current prototype is not PCI DSS, GDPR, CCPA, or SOC 2 compliant.
- Compliance topics are represented as design documentation and audit-log examples only.

## Security controls to implement before production

| Area | Production expectation | Prototype status |
|---|---|---|
| Authentication | Merchant login, API keys/OAuth, MFA | Not implemented |
| Authorization | RBAC by merchant, analyst, admin, support | Documented only |
| Data protection | Encryption in transit and at rest, tokenization | Documented only |
| Logging | Tamper-resistant audit logs and alert history | Demo JSONL audit log |
| Data minimization | Avoid unnecessary PII and payment data | Synthetic data only |
| Segmentation | Tenant isolation and least-privilege services | Documented only |
| Vulnerability management | SAST, dependency checks, pen tests | Not implemented |
| Incident response | Alerting, severity levels, customer communications | Documented only |

## Demo audit logging

The CLI generates:

```text
reports/audit_log.jsonl
```

The audit log records the scoring decision, factor names, and summarized input properties. It uses a short stable hash for `user_id` instead of writing raw user IDs into the log.

This demonstrates the governance principle, but it is not production-grade audit logging.

## Data handling principle

For a real product, DolAegis should treat fraud-risk data as sensitive even when it is not raw payment-card data. Device signals, location patterns, account history, chargeback history, and behavioral patterns can all become privacy-sensitive when combined.
