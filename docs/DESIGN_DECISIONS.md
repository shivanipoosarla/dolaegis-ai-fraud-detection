# Design Decisions

## Why the Project Uses Rules

The current implementation uses deterministic rules instead of a trained machine-learning model.

A useful fraud model requires labeled transaction outcomes, including confirmed fraud and legitimate transactions. The sample dataset in this repository is synthetic and too small to support meaningful model training or evaluation.

Using rules makes the prototype deterministic, testable, and explainable without presenting unvalidated predictions as machine-learning results.

## Why FastAPI Was Used

FastAPI provides request validation through Pydantic models and automatically generates OpenAPI documentation.

This allows the same scoring engine to be exposed through command-line and HTTP interfaces without duplicating the scoring logic.

## Why the Score Is Capped at 100

Multiple related risk signals can trigger for one transaction. For example, a country mismatch may occur alongside a high-risk-country flag.

The score is capped at 100 so that API consumers receive a predictable range. The score should not be interpreted as a calibrated probability that a transaction is fraudulent.

## Why Decisions Are Explainable

Each result includes the rules that contributed to its score.

This supports:

* Debugging rule behavior
* Reviewing blocked transactions
* Investigating false positives
* Supporting manual-review workflows

## Why User Identifiers Are Hashed

Audit outputs use hashed user identifiers to reduce the amount of directly identifying information written to generated logs.

Hashing is not the same as anonymization. A predictable identifier may still be vulnerable to re-identification, especially without a secret key or salt.

## Known Weaknesses

The thresholds are demonstration values and have not been evaluated against real fraud outcomes.

Some rules may produce false positives for:

* International customers
* Travelers using new devices
* New legitimate accounts
* High-value but valid purchases
* Transactions made during unusual hours

The current rules also treat some signals independently even when they may be correlated.

## What I Would Evaluate Next

With access to a suitable labeled dataset, the next steps would be:

1. Measure precision, recall, and false-positive rate.
2. Analyze the effectiveness of each individual rule.
3. Calibrate thresholds using validation data.
4. Compare the rules engine with a simple baseline model.
5. Add tests for correlated signals and boundary conditions.
6. Review whether country-based rules create unacceptable bias.
