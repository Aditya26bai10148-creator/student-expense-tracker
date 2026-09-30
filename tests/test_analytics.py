"""
test_analytics.py
Unit tests for financial analytics, totals, category distribution, and ASCII charting.
"""

import unittest
from src.analytics import FinancialAnalytics
from src.models import Transaction


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            Transaction(amount=10000.0, category="Allowance", tx_type="INCOME", date_str="2026-10-01"),
            Transaction(amount=3000.0, category="Food", tx_type="EXPENSE", date_str="2026-10-02"),
            Transaction(amount=1000.0, category="Travel", tx_type="EXPENSE", date_str="2026-10-03"),
            Transaction(amount=1000.0, category="Academics", tx_type="EXPENSE", date_str="2026-10-04"),
        ]

    def test_compute_totals(self):
        totals = FinancialAnalytics.compute_totals(self.transactions)
        self.assertEqual(totals["total_income"], 10000.0)
        self.assertEqual(totals["total_expense"], 5000.0)
        self.assertEqual(totals["net_savings"], 5000.0)
        self.assertEqual(totals["savings_rate"], 50.0)

    def test_category_breakdown(self):
        breakdown = FinancialAnalytics.category_breakdown(self.transactions)
        # Food is 3000 / 5000 = 60.0%
        self.assertIn("Food", breakdown)
        self.assertEqual(breakdown["Food"]["amount"], 3000.0)
        self.assertEqual(breakdown["Food"]["percentage"], 60.0)
        # Travel is 1000 / 5000 = 20.0%
        self.assertEqual(breakdown["Travel"]["percentage"], 20.0)

    def test_highest_spending_category(self):
        cat, amt = FinancialAnalytics.get_highest_spending_category(self.transactions)
        self.assertEqual(cat, "Food")
        self.assertEqual(amt, 3000.0)

    def test_ascii_bar_chart_generation(self):
        breakdown = FinancialAnalytics.category_breakdown(self.transactions)
        chart = FinancialAnalytics.generate_ascii_bar_chart(breakdown, bar_width=20)
        self.assertIn("Food", chart)
        self.assertIn("#", chart)
        self.assertIn("60.0%", chart)

    def test_empty_transactions(self):
        totals = FinancialAnalytics.compute_totals([])
        self.assertEqual(totals["total_income"], 0.0)
        self.assertEqual(totals["total_expense"], 0.0)
        self.assertEqual(totals["savings_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
