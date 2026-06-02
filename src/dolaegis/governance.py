from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Dict, Any

from .models import Transaction
from .risk_engine import RiskResult

GOVERNANCE_VERSION = "2026.06-demo"


def stable_hash(value: str) -> str:
    """Return a short stable SHA-256 hash for demo audit records.

    The prototype uses hashing so audit artifacts can demonstrate traceability
    without writing raw user identifiers into generated logs.
    """

    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return digest[:16]


def build_audit_record(tx: Transaction, result: RiskResult) -> Dict[str, Any]:
    """Build a privacy-aware audit record for one scored transaction.

    This is not a substitute for production audit logging. It is a portfolio
    demonstration of what should be recorded for explainability, review, and
    governance while minimizing sensitive fields.
    """

    return {
        "event_type": "fraud_score_decision",
        "governance_version": GOVERNANCE_VERSION,
        "transaction_id": tx.transaction_id,
        "user_hash": stable_hash(tx.user_id),
        "decision": result.decision,
        "risk_level": result.level,
        "risk_score": result.score,
        "factor_names": [factor.name for factor in result.factors],
        "factor_count": len(result.factors),
        "input_summary": {
            "amount_bucket": amount_bucket(tx.amount),
            "billing_shipping_match": tx.billing_country == tx.shipping_country,
            "ip_billing_match": tx.ip_country == tx.billing_country,
            "account_age_bucket": account_age_bucket(tx.account_age_days),
            "failed_login_count": tx.failed_login_count,
            "transactions_last_hour": tx.transactions_last_hour,
            "new_device": tx.new_device,
            "high_risk_country": tx.high_risk_country,
            "chargeback_history_count": tx.chargeback_history_count,
            "hour_of_day": tx.hour_of_day,
        },
    }


def amount_bucket(amount: float) -> str:
    if amount >= 1000:
        return "1000_plus"
    if amount >= 500:
        return "500_to_999"
    if amount >= 100:
        return "100_to_499"
    return "under_100"


def account_age_bucket(days: int) -> str:
    if days < 7:
        return "under_7_days"
    if days < 30:
        return "7_to_29_days"
    if days < 180:
        return "30_to_179_days"
    return "180_plus_days"


def write_audit_log(records: Iterable[Dict[str, Any]], path: Path) -> None:
    """Write newline-delimited JSON audit records."""

    path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            enriched = {"generated_at": generated_at, **record}
            handle.write(json.dumps(enriched, sort_keys=True) + "\n")
