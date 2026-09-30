"""
manager.py
The central business logic coordinator for PySpend.
Manages transaction CRUD, category budgets, threshold alert triggers, and filters.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from src.models import Budget, Transaction, ValidationError
from src.storage import StorageHandler


class ExpenseManager:
    """
    Coordinates application state, transaction operations, and budget enforcement.
    """
    DEFAULT_CATEGORIES = ["Food", "Academics", "Travel", "Entertainment", "Utilities", "Allowance", "General"]

    def __init__(self, storage: StorageHandler = None):
        self.storage = storage if storage else StorageHandler()
        self.transactions: List[Transaction] = []
        self.budgets: Dict[str, Budget] = {}
        self.load()

    def load(self) -> None:
        """Loads state from storage and initializes default budgets if none exist."""
        self.transactions, self.budgets = self.storage.load_data()
        if not self.budgets:
            # Helpful student defaults for new setups
            now = datetime.now()
            self.budgets["Food"] = Budget("Food", 4000.0, now.month, now.year)
            self.budgets["Academics"] = Budget("Academics", 1500.0, now.month, now.year)
            self.budgets["Travel"] = Budget("Travel", 800.0, now.month, now.year)

    def save(self) -> bool:
        """Persists current state to storage."""
        return self.storage.save_data(self.transactions, self.budgets)

    def add_transaction(self, amount: float, category: str, tx_type: str = "EXPENSE",
                        date_str: str = None, note: str = "") -> Tuple[Transaction, Optional[dict]]:
        """
        Creates, validates, records a new transaction, and evaluates budget alert thresholds.
        Returns a tuple of (new_transaction, budget_alert_info_if_applicable).
        """
        tx = Transaction(
            amount=amount,
            category=category,
            tx_type=tx_type,
            date_str=date_str,
            note=note
        )
        self.transactions.append(tx)
        self.save()

        # Check budget alert if this was an expense
        alert_info = None
        if tx.type == "EXPENSE":
            alert_info = self.get_category_budget_alert(tx.category, tx.date.month, tx.date.year)

        return tx, alert_info

    def delete_transaction(self, tx_id: str) -> bool:
        """
        Removes a transaction by its unique ID.
        Returns True if deleted, False if ID not found.
        """
        initial_count = len(self.transactions)
        self.transactions = [tx for tx in self.transactions if tx.id != tx_id]
        if len(self.transactions) < initial_count:
            self.save()
            return True
        return False

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        """Finds a single transaction by ID."""
        for tx in self.transactions:
            if tx.id == tx_id:
                return tx
        return None

    def get_all_transactions(self) -> List[Transaction]:
        """Returns all transactions sorted chronologically (newest first)."""
        return sorted(self.transactions, key=lambda t: t.date, reverse=True)

    def filter_transactions(self, category: str = None, month: int = None, 
                            year: int = None, tx_type: str = None) -> List[Transaction]:
        """
        Filters transactions based on optional category, month, year, and transaction type.
        """
        results = self.transactions

        if category:
            cat_clean = category.strip().title()
            results = [tx for tx in results if tx.category == cat_clean]

        if tx_type:
            type_clean = tx_type.strip().upper()
            results = [tx for tx in results if tx.type == type_clean]

        if month:
            results = [tx for tx in results if tx.date.month == int(month)]

        if year:
            results = [tx for tx in results if tx.date.year == int(year)]

        return sorted(results, key=lambda t: t.date, reverse=True)

    def set_budget(self, category: str, monthly_limit: float, 
                   month: int = None, year: int = None) -> Budget:
        """Sets or updates a monthly budget cap for a specific category."""
        budget = Budget(category=category, monthly_limit=monthly_limit, month=month, year=year)
        self.budgets[budget.category] = budget
        self.save()
        return budget

    def get_category_spent(self, category: str, month: int = None, year: int = None) -> float:
        """Computes total expenses spent in a given category for the specified month/year."""
        now = datetime.now()
        target_month = month if month else now.month
        target_year = year if year else now.year
        cat_clean = category.strip().title()

        total = sum(
            tx.amount for tx in self.transactions
            if tx.type == "EXPENSE" and tx.category == cat_clean
            and tx.date.month == target_month and tx.date.year == target_year
        )
        return round(total, 2)

    def get_category_budget_alert(self, category: str, month: int = None, year: int = None) -> Optional[dict]:
        """
        Evaluates whether a category has crossed the 80% caution or 100% exceeded threshold.
        Returns alert metadata dictionary or None if within normal range or no budget set.
        """
        cat_clean = category.strip().title()
        budget = self.budgets.get(cat_clean)
        if not budget:
            return None

        spent = self.get_category_spent(cat_clean, month, year)
        health = budget.evaluate_health(spent)

        if health["status"] in ("WARNING", "EXCEEDED"):
            return health
        return None

    def get_all_budgets_health(self, month: int = None, year: int = None) -> List[dict]:
        """
        Evaluates health for all configured category budgets.
        """
        now = datetime.now()
        target_month = month if month else now.month
        target_year = year if year else now.year

        report = []
        for cat, budget in sorted(self.budgets.items()):
            spent = self.get_category_spent(cat, target_month, target_year)
            health = budget.evaluate_health(spent)
            report.append(health)
        return report

    def export_csv(self, filename: str = "expenses_export.csv") -> str:
        """Exports all transactions to a CSV file and returns the path string."""
        path = self.storage.export_to_csv(self.transactions, filename)
        return str(path)
