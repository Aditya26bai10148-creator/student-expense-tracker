"""
analytics.py
Financial calculations, statistical aggregation, and terminal visualization routines for PySpend.
Generates metrics and ASCII horizontal bar charts using pure Python string manipulation.
"""

from typing import Dict, List, Tuple
from src.models import Transaction


class FinancialAnalytics:
    """
    Stateless analytical service providing summary metrics, category shares,
    and formatted terminal visual charts.
    """

    @staticmethod
    def compute_totals(transactions: List[Transaction]) -> dict:
        """
        Calculates Total Income, Total Expenses, Net Savings, and Savings Rate.
        """
        total_income = 0.0
        total_expense = 0.0

        for tx in transactions:
            if tx.type == "INCOME":
                total_income += tx.amount
            elif tx.type == "EXPENSE":
                total_expense += tx.amount

        total_income = round(total_income, 2)
        total_expense = round(total_expense, 2)
        net_savings = round(total_income - total_expense, 2)

        # Calculate savings rate percentage safely
        if total_income > 0:
            savings_rate = round((net_savings / total_income) * 100, 2)
        else:
            savings_rate = 0.0

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_savings": net_savings,
            "savings_rate": savings_rate
        }

    @staticmethod
    def category_breakdown(transactions: List[Transaction]) -> Dict[str, dict]:
        """
        Aggregates total spent per category and computes the percentage of total expense.
        Returns a sorted dictionary (highest expenditure first).
        """
        category_totals: Dict[str, float] = {}
        overall_expense = 0.0

        for tx in transactions:
            if tx.type == "EXPENSE":
                category_totals[tx.category] = category_totals.get(tx.category, 0.0) + tx.amount
                overall_expense += tx.amount

        breakdown = {}
        for cat, amount in sorted(category_totals.items(), key=lambda item: item[1], reverse=True):
            pct = round((amount / overall_expense) * 100, 1) if overall_expense > 0 else 0.0
            breakdown[cat] = {
                "amount": round(amount, 2),
                "percentage": pct
            }

        return breakdown

    @staticmethod
    def generate_ascii_bar_chart(category_breakdown: Dict[str, dict], bar_width: int = 30) -> str:
        """
        Generates a clean terminal ASCII horizontal bar chart representing expense distribution.
        Example:
        Food          [##############################] 64.6% (₹3,450.00)
        Travel        [########                      ] 17.2% (₹920.00)
        """
        if not category_breakdown:
            return "  No expense records available to render visual chart."

        max_spent = max(data["amount"] for data in category_breakdown.values())
        if max_spent <= 0:
            return "  All category expenditures are zero."

        lines = []
        for cat, data in category_breakdown.items():
            amount = data["amount"]
            pct = data["percentage"]
            # Scale bar length proportional to the highest spending category
            bar_len = int((amount / max_spent) * bar_width)
            bar_len = max(1, bar_len) if amount > 0 else 0
            empty_len = bar_width - bar_len

            bar = "#" * bar_len + " " * empty_len
            lines.append(f"  {cat:<14} [{bar}] {pct:>5.1f}% (₹{amount:,.2f})")

        return "\n".join(lines)

    @staticmethod
    def get_highest_spending_category(transactions: List[Transaction]) -> Tuple[str, float]:
        """
        Returns the category name and amount for the highest single expense category.
        """
        breakdown = FinancialAnalytics.category_breakdown(transactions)
        if not breakdown:
            return "None", 0.0
        first_cat = next(iter(breakdown))
        return first_cat, breakdown[first_cat]["amount"]
