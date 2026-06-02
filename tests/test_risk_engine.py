import unittest

from dolaegis.models import Transaction
from dolaegis.risk_engine import FraudRiskEngine


class FraudRiskEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = FraudRiskEngine()

    def test_low_risk_transaction_is_approved(self):
        tx = Transaction(
            transaction_id="tx_low",
            user_id="u1",
            amount=49.99,
            billing_country="US",
            shipping_country="US",
            ip_country="US",
            account_age_days=365,
            failed_login_count=0,
            transactions_last_hour=1,
            new_device=False,
            high_risk_country=False,
            chargeback_history_count=0,
            hour_of_day=12,
        )
        result = self.engine.score(tx)
        self.assertEqual(result.level, "low")
        self.assertEqual(result.decision, "approve")
        self.assertEqual(result.score, 0)

    def test_high_risk_transaction_is_blocked(self):
        tx = Transaction(
            transaction_id="tx_high",
            user_id="u2",
            amount=1500,
            billing_country="US",
            shipping_country="CA",
            ip_country="NG",
            account_age_days=2,
            failed_login_count=6,
            transactions_last_hour=7,
            new_device=True,
            high_risk_country=True,
            chargeback_history_count=3,
            hour_of_day=2,
        )
        result = self.engine.score(tx)
        self.assertEqual(result.level, "high")
        self.assertEqual(result.decision, "block")
        self.assertEqual(result.score, 100)
        factor_names = {factor.name for factor in result.factors}
        self.assertIn("high_amount", factor_names)
        self.assertIn("many_failed_logins", factor_names)
        self.assertIn("velocity_spike", factor_names)

    def test_medium_risk_transaction_goes_to_manual_review(self):
        tx = Transaction(
            transaction_id="tx_med",
            user_id="u3",
            amount=650,
            billing_country="US",
            shipping_country="CA",
            ip_country="US",
            account_age_days=20,
            failed_login_count=1,
            transactions_last_hour=1,
            new_device=True,
            high_risk_country=False,
            chargeback_history_count=0,
            hour_of_day=22,
        )
        result = self.engine.score(tx)
        self.assertEqual(result.level, "medium")
        self.assertEqual(result.decision, "manual_review")
        self.assertGreaterEqual(result.score, 40)
        self.assertLess(result.score, 70)


if __name__ == "__main__":
    unittest.main()
