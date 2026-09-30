"""
test_tracker.py
Unit tests for the Student Expense Tracker.
"""

import unittest
from src.tracker import ExpenseTracker
from src.models import Expense


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        """Runs before each test method."""
        self.tracker = ExpenseTracker(monthly_budget=3000.0)

    def test_add_expense(self):
        """Test adding an expense increases count and sets attributes correctly."""
        exp = self.tracker.add_expense(amount=250.0, category="Food", date="2026-09-10", note="Lunch")
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(exp.amount, 250.0)
        self.assertEqual(exp.category, "Food")
        self.assertEqual(exp.id, 1)

    def test_get_total_expenses(self):
        """Test calculating the total sum of all expenses."""
        self.tracker.add_expense(100.0, "Food", "2026-09-10")
        self.tracker.add_expense(200.0, "Books", "2026-09-11")
        self.tracker.add_expense(50.0, "Travel", "2026-09-12")
        self.assertEqual(self.tracker.get_total_expenses(), 350.0)

    def test_get_category_totals(self):
        """Test that category groupings calculate totals properly."""
        self.tracker.add_expense(100.0, "Food", "2026-09-10")
        self.tracker.add_expense(150.0, "Food", "2026-09-11")
        self.tracker.add_expense(80.0, "Travel", "2026-09-12")
        totals = self.tracker.get_category_totals()
        self.assertEqual(totals["Food"], 250.0)
        self.assertEqual(totals["Travel"], 80.0)

    def test_budget_status_ok(self):
        """Test budget status when under 80% capacity."""
        self.tracker.add_expense(1000.0, "Fees", "2026-09-10")
        status = self.tracker.check_budget_status()
        self.assertEqual(status["status"], "OK")
        self.assertEqual(status["remaining"], 2000.0)

    def test_budget_status_warning_and_exceeded(self):
        """Test warning threshold (>=80%) and exceeded threshold (>100%)."""
        # 2500 out of 3000 is 83.3% -> WARNING
        self.tracker.add_expense(2500.0, "Mess", "2026-09-10")
        status1 = self.tracker.check_budget_status()
        self.assertEqual(status1["status"], "WARNING")

        # 2500 + 700 = 3200 (> 3000) -> EXCEEDED
        self.tracker.add_expense(700.0, "Books", "2026-09-15")
        status2 = self.tracker.check_budget_status()
        self.assertEqual(status2["status"], "EXCEEDED")
        self.assertEqual(status2["remaining"], -200.0)


if __name__ == "__main__":
    unittest.main()
