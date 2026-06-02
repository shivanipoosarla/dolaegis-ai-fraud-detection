# API Security Notes

The API in this repository is a local mock service. It intentionally avoids real authentication or payment integrations so it can be run easily by reviewers.

Before production, the API would need:

- API key or OAuth-based authentication.
- Merchant/tenant scoping on every request.
- Request signing or replay protection for payment-provider callbacks.
- Rate limiting and bot protection.
- Structured error handling that does not leak sensitive internals.
- Request/response logging with sensitive-field redaction.
- API versioning.
- Input validation for all fields and schemas.
- Dependency scanning and CI security checks.

Current demo endpoints:

```text
GET  /health
POST /score
POST /batch-score
```

The `/score` and `/batch-score` responses include an `audit` object to demonstrate how decision evidence could be preserved without logging raw user identifiers.
