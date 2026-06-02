# API Spec

DolAegis includes a small FastAPI service to model the SaaS/API layer described in the product strategy.

## Run locally

```bash
PYTHONPATH=src uvicorn dolaegis.api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### `GET /health`

Returns service health.

### `POST /score`

Scores one transaction and returns an explainable decision.

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d @api-examples/score_request.json
```

### `POST /batch-score`

Scores multiple transactions and returns a summary plus per-transaction results.

```bash
curl -X POST http://127.0.0.1:8000/batch-score \
  -H "Content-Type: application/json" \
  -d @api-examples/batch_score_request.json
```

## Scope

This is an API prototype. It does not connect to live Shopify, WooCommerce, Stripe, PayPal, or banking systems. The current risk engine is rules-based and explainable; a later version could add a trained model behind the same response contract.


## Audit object

The `/score` endpoint returns a demo `audit` object with:

- `event_type`
- `governance_version`
- `transaction_id`
- hashed `user_hash`
- decision, risk level, and score
- factor names
- summarized input properties

This is a prototype governance artifact, not a production audit-log implementation.
