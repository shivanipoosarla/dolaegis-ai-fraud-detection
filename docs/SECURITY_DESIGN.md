# Security Design

## Current Scope

DolAegis is a local educational prototype that processes synthetic transaction data.

The main exposed component is a FastAPI service with health, single-transaction scoring, and batch-scoring endpoints.

## Implemented Controls

The current implementation includes:

* Pydantic request validation
* Synthetic sample data
* Hashed user identifiers in generated audit records
* Unit tests
* Automated test execution through GitHub Actions
* No credentials or API secrets required for local execution

## Known Security Limitations

The API currently has:

* No authentication
* No authorization
* No rate limiting
* No tenant isolation
* No persistent database
* No tamper-resistant audit storage
* No transport-security configuration within the application
* No production secrets-management integration

The API should therefore only be run in a local or controlled development environment.

## Data Handling

The included dataset is synthetic and should not contain real payment-card or customer information.

A production implementation should minimize stored transaction data and define retention periods for:

* Transaction inputs
* Risk results
* Analyst decisions
* Audit records
* User identifiers

Hashing an identifier reduces direct exposure but does not guarantee anonymity.

## Primary Threats

### Malformed or Oversized Requests

An attacker could submit invalid or unusually large request bodies.

Current mitigation:

* Pydantic schema validation

Required production controls:

* Request-size limits
* Rate limiting
* Authentication
* Reverse-proxy protections

### Unauthorized Scoring Requests

The API currently accepts requests without verifying the caller.

Required production controls:

* API-key or OAuth-based authentication
* Authorization policies
* Tenant separation
* Request logging

### Audit-Log Modification

Generated JSONL logs are ordinary local files and can be modified or deleted.

Required production controls:

* Append-only storage
* Access controls
* Integrity verification
* Centralized log retention

### Rule Manipulation

Changes to rule thresholds could alter scoring behavior.

Required production controls:

* Version-controlled policies
* Change review
* Policy versions included in results
* Tests for threshold changes

## Dependency and Deployment Security

A production deployment should add:

* Dependency vulnerability scanning
* Container-image scanning
* Secret scanning
* HTTPS termination
* Restricted network access
* Non-root container execution
* Logging and alerting
* Regular patching

## Compliance

This repository does not claim compliance with PCI DSS, GDPR, CCPA, SOC 2, ISO 27001, or any other standard.

Compliance would depend on the complete deployed system, its organizational controls, data flows, infrastructure, vendors, and operating procedures—not this source repository alone.
