from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict

from .models import Transaction


@dataclass(frozen=True)
class RiskFactor:
    name: str
    points: int
    explanation: str


@dataclass(frozen=True)
class RiskResult:
    transaction_id: str
    user_id: str
    score: int
    level: str
    decision: str
    factors: List[RiskFactor]

    def to_dict(self) -> Dict[str, object]:
        data = asdict(self)
        data["factors"] = [asdict(factor) for factor in self.factors]
        return data


class FraudRiskEngine:
    """Explainable fraud-risk scoring engine.

    The first portfolio version is intentionally rule-based. It demonstrates
    product thinking and explainability without pretending to be a production ML
    fraud model. A later version can add a trained model behind the same result
    interface.
    """

    def score(self, tx: Transaction) -> RiskResult:
        factors: List[RiskFactor] = []

        if tx.amount >= 1000:
            factors.append(RiskFactor("high_amount", 25, "Transaction amount is at or above 1000."))
        elif tx.amount >= 500:
            factors.append(RiskFactor("medium_high_amount", 15, "Transaction amount is at or above 500."))

        if tx.billing_country and tx.shipping_country and tx.billing_country != tx.shipping_country:
            factors.append(RiskFactor("billing_shipping_mismatch", 15, "Billing and shipping countries differ."))

        if tx.ip_country and tx.billing_country and tx.ip_country != tx.billing_country:
            factors.append(RiskFactor("ip_billing_mismatch", 15, "IP country differs from billing country."))

        if tx.account_age_days < 7:
            factors.append(RiskFactor("new_account", 15, "Account is less than 7 days old."))
        elif tx.account_age_days < 30:
            factors.append(RiskFactor("young_account", 8, "Account is less than 30 days old."))

        if tx.failed_login_count >= 5:
            factors.append(RiskFactor("many_failed_logins", 20, "Five or more failed login attempts were observed."))
        elif tx.failed_login_count >= 3:
            factors.append(RiskFactor("failed_login_spike", 10, "Three or more failed login attempts were observed."))

        if tx.transactions_last_hour >= 5:
            factors.append(RiskFactor("velocity_spike", 20, "Five or more transactions occurred in the last hour."))
        elif tx.transactions_last_hour >= 3:
            factors.append(RiskFactor("elevated_velocity", 10, "Three or more transactions occurred in the last hour."))

        if tx.new_device:
            factors.append(RiskFactor("new_device", 10, "Transaction originated from a new device."))

        if tx.high_risk_country:
            factors.append(RiskFactor("high_risk_country", 15, "Transaction is associated with a high-risk country flag."))

        if tx.chargeback_history_count >= 2:
            factors.append(RiskFactor("repeated_chargebacks", 20, "User has two or more prior chargebacks."))
        elif tx.chargeback_history_count == 1:
            factors.append(RiskFactor("prior_chargeback", 10, "User has one prior chargeback."))

        if 0 <= tx.hour_of_day <= 5:
            factors.append(RiskFactor("unusual_hour", 5, "Transaction occurred between midnight and 5 AM."))

        score = min(100, sum(f.points for f in factors))
        level, decision = self._classify(score)
        return RiskResult(
            transaction_id=tx.transaction_id,
            user_id=tx.user_id,
            score=score,
            level=level,
            decision=decision,
            factors=factors,
        )

    @staticmethod
    def _classify(score: int) -> tuple[str, str]:
        if score >= 70:
            return "high", "block"
        if score >= 40:
            return "medium", "manual_review"
        return "low", "approve"
