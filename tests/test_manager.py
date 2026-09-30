"""
test_manager.py
Unit tests for ExpenseManager business logic, CRUD operations, and threshold alerts.
"""

import tempfile
import unittest

from src.manager import ExpenseManager
from src.storage import StorageHandler


class TestExpenseManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageHandler(data_dir=self.temp_dir.name, filename="test_expenses.json")
        self.manager = ExpenseManager(storage=self.storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_get_transaction(self):
        tx, alert = self.manager.add_transaction(
            amount=500.0,
            category="Academics",
            tx_type="EXPENSE",
            date_str="2026-10-05",
            note="Books"
        )
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, 500.0)

        # Retrieve by ID
        fetched = self.manager.get_transaction(tx.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.note, "Books")

    def test_delete_transaction(self):
        tx, _ = self.manager.add_transaction(amount=200.0, category="Food")
        self.assertTrue(self.manager.delete_transaction(tx.id))
        self.assertIsNone(self.manager.get_transaction(tx.id))
        # Deleting non-existent should return False
        self.assertFalse(self.manager.delete_transaction("non_existent_id"))

    def test_budget_threshold_warning_triggered(self):
        # Set Food budget limit to 1000.0
        self.manager.set_budget("Food", 1000.0, month=10, year=2026)

        # Spend 700 (70%) -> No warning
        _, alert1 = self.manager.add_transaction(amount=700.0, category="Food", date_str="2026-10-02")
        self.assertIsNone(alert1)

        # Spend another 150 (Total 850, 85%) -> WARNING alert
        _, alert2 = self.manager.add_transaction(amount=150.0, category="Food", date_str="2026-10-03")
        self.assertIsNotNone(alert2)
        self.assertEqual(alert2["status"], "WARNING")
        self.assertEqual(alert2["utilization_pct"], 85.0)

        # Spend another 200 (Total 1050, 105%) -> EXCEEDED alert
        _, alert3 = self.manager.add_transaction(amount=200.0, category="Food", date_str="2026-10-04")
        self.assertIsNotNone(alert3)
        self.assertEqual(alert3["status"], "EXCEEDED")
        self.assertEqual(alert3["remaining"], -50.0)

    def test_filter_transactions(self):
        self.manager.add_transaction(amount=100.0, category="Food", tx_type="EXPENSE", date_str="2026-09-10")
        self.manager.add_transaction(amount=200.0, category="Travel", tx_type="EXPENSE", date_str="2026-10-15")
        self.manager.add_transaction(amount=5000.0, category="Allowance", tx_type="INCOME", date_str="2026-10-01")

        # Filter by category
        food_txs = self.manager.filter_transactions(category="Food")
        self.assertEqual(len(food_txs), 1)

        # Filter by month
        oct_txs = self.manager.filter_transactions(month=10)
        self.assertEqual(len(oct_txs), 2)

        # Filter by type
        incomes = self.manager.filter_transactions(tx_type="INCOME")
        self.assertEqual(len(incomes), 1)


if __name__ == "__main__":
    unittest.main()
