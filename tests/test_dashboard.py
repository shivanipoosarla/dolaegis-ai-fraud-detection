import unittest

from dolaegis.dashboard import build_dashboard_html, summarize_results
from dolaegis.models import Transaction
from dolaegis.risk_engine import FraudRiskEngine


class DashboardTests(unittest.TestCase):
    def setUp(self):
        engine = FraudRiskEngine()
        self.results = [
            engine.score(
                Transaction(
                    transaction_id="tx_low",
                    user_id="u1",
                    amount=50,
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
            ),
            engine.score(
                Transaction(
                    transaction_id="tx_high",
                    user_id="u2",
                    amount=1500,
                    billing_country="US",
                    shipping_country="CA",
                    ip_country="NG",
                    account_age_days=2,
                    failed_login_count=7,
                    transactions_last_hour=6,
                    new_device=True,
                    high_risk_country=True,
                    chargeback_history_count=2,
                    hour_of_day=1,
                )
            ),
        ]

    def test_summary_counts_decisions(self):
        summary = summarize_results(self.results)
        self.assertEqual(summary["transactions_analyzed"], 2)
        self.assertEqual(summary["high_risk"], 1)
        self.assertEqual(summary["approved"], 1)
        self.assertEqual(summary["blocked"], 1)

    def test_dashboard_html_contains_key_sections(self):
        html = build_dashboard_html(self.results)
        self.assertIn("DolAegis Fraud Risk Dashboard", html)
        self.assertIn("Transaction Review Table", html)
        self.assertIn("tx_high", html)
        self.assertIn("Top Risk Factors", html)
        self.assertIn("Prototype scope", html)


if __name__ == "__main__":
    unittest.main()
