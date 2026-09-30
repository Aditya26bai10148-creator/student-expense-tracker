"""
tracker.py
Core tracking logic for student expenses, category summaries, and budget limits.
"""

from src.models import Expense

class ExpenseTracker:
    def __init__(self, expenses=None, monthly_budget=5000.0):
        self.expenses = expenses if expenses is not None else []
        self.monthly_budget = float(monthly_budget)

    def add_expense(self, amount: float, category: str, date: str, note: str = "") -> Expense:
        """Adds a new expense and auto-assigns an ID."""
        new_id = len(self.expenses) + 1
        exp = Expense(amount, category, date, note, new_id)
        self.expenses.append(exp)
        return exp

    def get_total_expenses(self) -> float:
        """Calculates total money spent across all expenses."""
        return sum(exp.amount for exp in self.expenses)

    def get_category_totals(self) -> dict:
        """Calculates the total money spent per category."""
        totals = {}
        for exp in self.expenses:
            totals[exp.category] = totals.get(exp.category, 0.0) + exp.amount
        return totals

    def check_budget_status(self) -> dict:
        """
        Evaluates the current total spending against the monthly budget limit.
        Returns budget amount, spent amount, remaining amount, and status string.
        """
        spent = self.get_total_expenses()
        remaining = self.monthly_budget - spent
        percent_used = (spent / self.monthly_budget) * 100 if self.monthly_budget > 0 else 0

        if spent > self.monthly_budget:
            status = "EXCEEDED"
        elif percent_used >= 80:
            status = "WARNING"
        else:
            status = "OK"

        return {
            "budget": self.monthly_budget,
            "spent": spent,
            "remaining": remaining,
            "percent_used": round(percent_used, 1),
            "status": status
        }
