import unittest

from fastapi.testclient import TestClient

from dolaegis.api import app


class DolAegisApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_score_endpoint_returns_high_risk_decision(self):
        payload = {
            "transaction_id": "tx_api_high",
            "user_id": "user_1",
            "amount": 1500,
            "billing_country": "US",
            "shipping_country": "CA",
            "ip_country": "NG",
            "account_age_days": 2,
            "failed_login_count": 6,
            "transactions_last_hour": 7,
            "new_device": True,
            "high_risk_country": True,
            "chargeback_history_count": 2,
            "hour_of_day": 2,
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("audit", body)
        self.assertIn("user_hash", body["audit"])
        result = body["result"]
        self.assertEqual(result["level"], "high")
        self.assertEqual(result["decision"], "block")
        self.assertGreaterEqual(result["score"], 70)

    def test_batch_score_endpoint_returns_summary(self):
        payload = {
            "transactions": [
                {
                    "transaction_id": "tx_api_high",
                    "user_id": "user_1",
                    "amount": 1500,
                    "billing_country": "US",
                    "shipping_country": "CA",
                    "ip_country": "NG",
                    "account_age_days": 2,
                    "failed_login_count": 6,
                    "transactions_last_hour": 7,
                    "new_device": True,
                    "high_risk_country": True,
                    "chargeback_history_count": 2,
                    "hour_of_day": 2,
                },
                {
                    "transaction_id": "tx_api_low",
                    "user_id": "user_2",
                    "amount": 59.99,
                    "billing_country": "US",
                    "shipping_country": "US",
                    "ip_country": "US",
                    "account_age_days": 300,
                    "failed_login_count": 0,
                    "transactions_last_hour": 1,
                    "new_device": False,
                    "high_risk_country": False,
                    "chargeback_history_count": 0,
                    "hour_of_day": 15,
                },
            ]
        }
        response = self.client.post("/batch-score", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["summary"]["transactions_analyzed"], 2)
        self.assertEqual(body["summary"]["high_risk"], 1)
        self.assertEqual(body["summary"]["approved"], 1)
        self.assertEqual(len(body["audit"]), 2)


if __name__ == "__main__":
    unittest.main()
