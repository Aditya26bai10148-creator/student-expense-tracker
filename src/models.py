"""
models.py
Defines the core data entities and domain classes for PySpend:
- Transaction
- Budget
- Custom domain exceptions
"""

from datetime import datetime
import uuid


class ExpenseTrackerError(Exception):
    """Base exception class for the PySpend application."""
    pass


class ValidationError(ExpenseTrackerError):
    """Raised when an input value fails validation rules."""
    pass


class BudgetExceededWarning(ExpenseTrackerError):
    """Raised or flagged when an expense exceeds defined budget thresholds."""
    pass


class Transaction:
    """
    Represents an individual financial transaction (Expense or Income).
    """
    VALID_TYPES = ("EXPENSE", "INCOME")

    def __init__(self, amount: float, category: str, tx_type: str = "EXPENSE", 
                 date_str: str = None, note: str = "", tx_id: str = None):
        """
        Initializes a Transaction object with validation.
        """
        # Defensive amount validation
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValidationError(f"Transaction amount must be a positive number, got: {amount}")
        
        tx_type_upper = str(tx_type).strip().upper()
        if tx_type_upper not in self.VALID_TYPES:
            raise ValidationError(f"Invalid transaction type '{tx_type}'. Must be EXPENSE or INCOME.")

        category_clean = str(category).strip().title()
        if not category_clean:
            raise ValidationError("Category name cannot be empty.")

        # Parse and format date (defaulting to today in YYYY-MM-DD)
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.")
        else:
            parsed_date = datetime.now().date()

        self.id = tx_id if tx_id else f"tx_{uuid.uuid4().hex[:6]}"
        self.amount = round(float(amount), 2)
        self.category = category_clean
        self.type = tx_type_upper
        self.date = parsed_date
        self.note = str(note).strip()

    @property
    def date_str(self) -> str:
        """Returns the ISO formatted date string (YYYY-MM-DD)."""
        return self.date.strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """Serializes the Transaction object into a dictionary for JSON/CSV storage."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "type": self.type,
            "date": self.date_str,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Instantiates a Transaction object from a dictionary."""
        return cls(
            amount=data.get("amount", 0.0),
            category=data.get("category", "General"),
            tx_type=data.get("type", "EXPENSE"),
            date_str=data.get("date"),
            note=data.get("note", ""),
            tx_id=data.get("id")
        )

    def __str__(self) -> str:
        symbol = "-" if self.type == "EXPENSE" else "+"
        return f"[{self.date_str}] {self.id} | {self.category:<12} | {symbol}₹{self.amount:>8.2f} | {self.note}"

    def __repr__(self) -> str:
        return f"Transaction(id='{self.id}', amount={self.amount}, category='{self.category}', type='{self.type}')"


class Budget:
    """
    Represents a monthly spending budget allocated to a specific category.
    """
    def __init__(self, category: str, monthly_limit: float, month: int = None, year: int = None):
        cat_clean = str(category).strip().title()
        if not cat_clean:
            raise ValidationError("Budget category cannot be empty.")
        
        if not isinstance(monthly_limit, (int, float)) or monthly_limit <= 0:
            raise ValidationError(f"Monthly limit must be a positive number, got: {monthly_limit}")

        now = datetime.now()
        self.category = cat_clean
        self.monthly_limit = round(float(monthly_limit), 2)
        self.month = int(month) if month else now.month
        self.year = int(year) if year else now.year

    def evaluate_health(self, total_spent: float) -> dict:
        """
        Evaluates the health of the budget against the total spent amount.
        Returns a dictionary with spent, remaining, percentage, and alert status.
        """
        spent = round(float(total_spent), 2)
        remaining = round(self.monthly_limit - spent, 2)
        utilization_pct = round((spent / self.monthly_limit) * 100, 2) if self.monthly_limit > 0 else 0.0

        if utilization_pct > 100.0:
            status = "EXCEEDED"
            badge = "[X] EXCEEDED"
        elif utilization_pct >= 80.0:
            status = "WARNING"
            badge = "[!] WARNING (>80%)"
        else:
            status = "OK"
            badge = "[OK] Normal"

        return {
            "category": self.category,
            "monthly_limit": self.monthly_limit,
            "spent": spent,
            "remaining": remaining,
            "utilization_pct": utilization_pct,
            "status": status,
            "badge": badge
        }

    def to_dict(self) -> dict:
        """Serializes the Budget object to a dictionary."""
        return {
            "category": self.category,
            "monthly_limit": self.monthly_limit,
            "month": self.month,
            "year": self.year
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Reconstitutes a Budget instance from a dictionary."""
        return cls(
            category=data.get("category", "General"),
            monthly_limit=data.get("monthly_limit", 1000.0),
            month=data.get("month"),
            year=data.get("year")
        )

    def __str__(self) -> str:
        return f"Budget({self.category}: Limit=₹{self.monthly_limit:.2f}, Period={self.month:02d}/{self.year})"
