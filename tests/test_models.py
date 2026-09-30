"""
test_models.py
Unit tests for domain entities: Transaction and Budget.
"""

import unittest
from src.models import Budget, Transaction, ValidationError


class TestModels(unittest.TestCase):
    def test_valid_transaction_creation(self):
        tx = Transaction(amount=250.0, category="Food", tx_type="EXPENSE", date_str="2026-10-05", note="Lunch")
        self.assertEqual(tx.amount, 250.0)
        self.assertEqual(tx.category, "Food")
        self.assertEqual(tx.type, "EXPENSE")
        self.assertEqual(tx.date_str, "2026-10-05")
        self.assertEqual(tx.note, "Lunch")
        self.assertTrue(tx.id.startswith("tx_"))

    def test_invalid_negative_amount(self):
        with self.assertRaises(ValidationError):
            Transaction(amount=-50.0, category="Food")

    def test_invalid_zero_amount(self):
        with self.assertRaises(ValidationError):
            Transaction(amount=0.0, category="Food")

    def test_invalid_transaction_type(self):
        with self.assertRaises(ValidationError):
            Transaction(amount=100.0, category="Food", tx_type="INVALID_TYPE")

    def test_invalid_date_format(self):
        with self.assertRaises(ValidationError):
            Transaction(amount=100.0, category="Food", date_str="05/10/2026")

    def test_transaction_serialization_roundtrip(self):
        tx1 = Transaction(amount=320.50, category="Travel", tx_type="EXPENSE", date_str="2026-10-01", note="Bus ticket")
        tx_dict = tx1.to_dict()
        tx2 = Transaction.from_dict(tx_dict)
        self.assertEqual(tx1.id, tx2.id)
        self.assertEqual(tx1.amount, tx2.amount)
        self.assertEqual(tx1.category, tx2.category)
        self.assertEqual(tx1.date_str, tx2.date_str)

    def test_budget_health_evaluation(self):
        budget = Budget(category="Food", monthly_limit=1000.0, month=10, year=2026)

        # Under 80% -> OK
        h_ok = budget.evaluate_health(500.0)
        self.assertEqual(h_ok["status"], "OK")
        self.assertEqual(h_ok["remaining"], 500.0)
        self.assertEqual(h_ok["utilization_pct"], 50.0)

        # At or above 80% -> WARNING
        h_warn = budget.evaluate_health(850.0)
        self.assertEqual(h_warn["status"], "WARNING")
        self.assertEqual(h_warn["remaining"], 150.0)

        # Above 100% -> EXCEEDED
        h_exceeded = budget.evaluate_health(1200.0)
        self.assertEqual(h_exceeded["status"], "EXCEEDED")
        self.assertEqual(h_exceeded["remaining"], -200.0)
        self.assertEqual(h_exceeded["utilization_pct"], 120.0)


if __name__ == "__main__":
    unittest.main()
