from __future__ import annotations

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .models import Transaction
from .risk_engine import FraudRiskEngine
from .governance import build_audit_record


class TransactionRequest(BaseModel):
    """API request model for a transaction scoring request."""

    transaction_id: str = Field(..., examples=["tx_1001"])
    user_id: str = Field(..., examples=["user_42"])
    amount: float = Field(..., ge=0, examples=[749.99])
    billing_country: str = Field(..., min_length=2, max_length=2, examples=["US"])
    shipping_country: str = Field(..., min_length=2, max_length=2, examples=["US"])
    ip_country: str = Field(..., min_length=2, max_length=2, examples=["US"])
    account_age_days: int = Field(..., ge=0, examples=[45])
    failed_login_count: int = Field(..., ge=0, examples=[0])
    transactions_last_hour: int = Field(..., ge=0, examples=[1])
    new_device: bool = Field(..., examples=[False])
    high_risk_country: bool = Field(..., examples=[False])
    chargeback_history_count: int = Field(..., ge=0, examples=[0])
    hour_of_day: int = Field(..., ge=0, le=23, examples=[14])

    def to_transaction(self) -> Transaction:
        return Transaction(
            transaction_id=self.transaction_id,
            user_id=self.user_id,
            amount=self.amount,
            billing_country=self.billing_country.upper(),
            shipping_country=self.shipping_country.upper(),
            ip_country=self.ip_country.upper(),
            account_age_days=self.account_age_days,
            failed_login_count=self.failed_login_count,
            transactions_last_hour=self.transactions_last_hour,
            new_device=self.new_device,
            high_risk_country=self.high_risk_country,
            chargeback_history_count=self.chargeback_history_count,
            hour_of_day=self.hour_of_day,
        )


class BatchScoreRequest(BaseModel):
    transactions: List[TransactionRequest]


engine = FraudRiskEngine()

app = FastAPI(
    title="DolAegis Fraud Scoring API",
    description=(
        "REST-style API prototype for scoring SMB e-commerce transactions. "
        "This demo uses explainable rules, not a production ML fraud model."
    ),
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "dolaegis-fraud-scoring-api"}


@app.post("/score")
def score_transaction(request: TransactionRequest) -> dict[str, object]:
    tx = request.to_transaction()
    result = engine.score(tx)
    return {"result": result.to_dict(), "audit": build_audit_record(tx, result)}


@app.post("/batch-score")
def batch_score(request: BatchScoreRequest) -> dict[str, object]:
    transactions = [item.to_transaction() for item in request.transactions]
    scored = [engine.score(tx) for tx in transactions]
    results = [result.to_dict() for result in scored]
    audit_records = [build_audit_record(tx, result) for tx, result in zip(transactions, scored)]
    high = sum(1 for item in results if item["level"] == "high")
    manual_review = sum(1 for item in results if item["decision"] == "manual_review")
    approved = sum(1 for item in results if item["decision"] == "approve")
    return {
        "summary": {
            "transactions_analyzed": len(results),
            "high_risk": high,
            "manual_review": manual_review,
            "approved": approved,
        },
        "results": results,
        "audit": audit_records,
    }
