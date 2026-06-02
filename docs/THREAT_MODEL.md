# Threat Model

## Assets

- Merchant transaction data
- Fraud decisions and risk scores
- API keys and integration credentials
- Audit logs
- Dashboard access
- Scoring policy/model artifacts

## Likely threats

| Threat | Example | Mitigation direction |
|---|---|---|
| Unauthorized API use | Attacker submits or reads transactions | API keys/OAuth, rate limits, tenant isolation |
| Data leakage | Support user sees wrong merchant data | RBAC, audit logging, row-level access control |
| Model/rule manipulation | Insider changes thresholds to approve risky orders | Change control, policy versioning, approvals |
| Evasion | Fraudster tests patterns to stay below thresholds | velocity controls, anomaly detection, adaptive rules |
| Availability attack | Bot traffic overloads scoring API | rate limiting, autoscaling, caching, WAF |
| False positives | Good customers blocked | manual review queue, threshold tuning, feedback loop |
| Compliance failure | Retaining sensitive data too long | retention policies, deletion workflows, evidence collection |

## Trust boundaries

```text
Merchant Platform / Payment Provider
  -> Public API boundary
  -> Scoring service
  -> Risk report/dashboard
  -> Audit and governance store
```

The prototype models only the scoring service and static output layers. Authentication, tenant isolation, database persistence, and real payment-provider integrations are out of scope.
