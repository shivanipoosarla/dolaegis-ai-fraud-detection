import json
import tempfile
import unittest
from pathlib import Path

from dolaegis.governance import stable_hash, build_audit_record, write_audit_log
from dolaegis.models import Transaction
from dolaegis.risk_engine import FraudRiskEngine


class GovernanceTests(unittest.TestCase):
    def _tx(self):
        return Transaction(
            transaction_id="tx_gov",
            user_id="customer-123",
            amount=1200,
            billing_country="US",
            shipping_country="CA",
            ip_country="NG",
            account_age_days=2,
            failed_login_count=6,
            transactions_last_hour=7,
            new_device=True,
            high_risk_country=True,
            chargeback_history_count=2,
            hour_of_day=3,
        )

    def test_stable_hash_redacts_raw_user_id(self):
        first = stable_hash("customer-123")
        second = stable_hash("customer-123")
        self.assertEqual(first, second)
        self.assertNotEqual(first, "customer-123")
        self.assertEqual(len(first), 16)

    def test_audit_record_contains_decision_without_raw_user_id(self):
        tx = self._tx()
        result = FraudRiskEngine().score(tx)
        record = build_audit_record(tx, result)
        self.assertEqual(record["event_type"], "fraud_score_decision")
        self.assertEqual(record["transaction_id"], "tx_gov")
        self.assertNotEqual(record["user_hash"], "customer-123")
        self.assertEqual(record["decision"], "block")
        self.assertIn("factor_names", record)
        self.assertIn("input_summary", record)

    def test_write_audit_log_outputs_jsonl(self):
        tx = self._tx()
        result = FraudRiskEngine().score(tx)
        record = build_audit_record(tx, result)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            write_audit_log([record], path)
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            parsed = json.loads(lines[0])
            self.assertEqual(parsed["event_type"], "fraud_score_decision")
            self.assertIn("generated_at", parsed)


if __name__ == "__main__":
    unittest.main()
