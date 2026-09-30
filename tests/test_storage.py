"""
test_storage.py
Unit tests for JSON data persistence, safe saving, and CSV export.
"""

from pathlib import Path
import tempfile
import unittest

from src.models import Budget, Transaction
from src.storage import StorageHandler


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = StorageHandler(data_dir=self.temp_dir.name, filename="test_expenses.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_reload_data(self):
        tx1 = Transaction(amount=500.0, category="Food", tx_type="EXPENSE", date_str="2026-10-01", note="Lunch")
        b1 = Budget(category="Food", monthly_limit=2000.0, month=10, year=2026)

        # Save
        self.storage.save_data([tx1], {"Food": b1})

        # Reload
        loaded_txs, loaded_budgets = self.storage.load_data()
        self.assertEqual(len(loaded_txs), 1)
        self.assertEqual(loaded_txs[0].amount, 500.0)
        self.assertEqual(loaded_txs[0].category, "Food")
        self.assertIn("Food", loaded_budgets)
        self.assertEqual(loaded_budgets["Food"].monthly_limit, 2000.0)

    def test_export_to_csv(self):
        tx1 = Transaction(amount=350.0, category="Travel", tx_type="EXPENSE", date_str="2026-10-02")
        export_path = self.storage.export_to_csv([tx1], "test_export.csv")
        self.assertTrue(Path(export_path).exists())

        with open(export_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("ID,Date,Type,Category,Amount (INR),Note", content)
            self.assertIn("Travel", content)
            self.assertIn("350.00", content)

    def test_handle_corrupted_json_recovery(self):
        # Write corrupted raw text to the file
        with open(self.storage.filepath, "w", encoding="utf-8") as f:
            f.write("{corrupt json content...")

        txs, budgets = self.storage.load_data()
        # Should gracefully return empty state rather than crash
        self.assertEqual(txs, [])
        self.assertEqual(budgets, {})


if __name__ == "__main__":
    unittest.main()
