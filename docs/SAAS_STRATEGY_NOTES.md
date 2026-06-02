# SaaS Strategy Notes

This repository implements a small technical slice of the DolAegis strategy: transaction ingestion, risk scoring, explainable decisions, and review-ready reporting.

## Product intent

DolAegis is positioned as an SMB-first fraud detection SaaS. The strategy emphasizes:

- Real-time risk scoring
- Explainable decisions
- API-first integrations
- Plug-and-play onboarding for SMB merchants
- Fraud-loss and chargeback reduction
- Future integrations with platforms such as Shopify, WooCommerce, Stripe, and PayPal

## Why the first implementation is rules-based

The presentation describes a hybrid direction: rule-based controls first, then ML and continuous learning as the intelligence layer matures. This repo follows that path by implementing an explainable rules engine before adding any model-training claims.

## Future SaaS capabilities

- Merchant authentication and RBAC
- API keys and tenant isolation
- Database persistence
- Dashboard and alert queue
- Integration connectors
- Audit logs and compliance evidence collection
- Model-training and drift-monitoring experiments
