from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Transaction:
    """Normalized transaction data used by the risk engine.

    This model intentionally keeps fields simple so the demo can run from a CSV
    without external databases or API credentials.
    """

    transaction_id: str
    user_id: str
    amount: float
    billing_country: str
    shipping_country: str
    ip_country: str
    account_age_days: int
    failed_login_count: int
    transactions_last_hour: int
    new_device: bool
    high_risk_country: bool
    chargeback_history_count: int
    hour_of_day: int

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Transaction":
        return cls(
            transaction_id=str(row.get("transaction_id", "")).strip(),
            user_id=str(row.get("user_id", "")).strip(),
            amount=_to_float(row.get("amount")),
            billing_country=str(row.get("billing_country", "")).strip().upper(),
            shipping_country=str(row.get("shipping_country", "")).strip().upper(),
            ip_country=str(row.get("ip_country", "")).strip().upper(),
            account_age_days=_to_int(row.get("account_age_days")),
            failed_login_count=_to_int(row.get("failed_login_count")),
            transactions_last_hour=_to_int(row.get("transactions_last_hour")),
            new_device=_to_bool(row.get("new_device")),
            high_risk_country=_to_bool(row.get("high_risk_country")),
            chargeback_history_count=_to_int(row.get("chargeback_history_count")),
            hour_of_day=max(0, min(23, _to_int(row.get("hour_of_day")))),
        )
