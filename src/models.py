"""
models.py
Defines the Expense class for the Student Expense Tracker.
"""

class Expense:
    def __init__(self, amount: float, category: str, date: str, note: str = "", expense_id: int = 0):
        self.id = expense_id
        self.amount = float(amount)
        self.category = category.strip().title()
        self.date = date.strip()
        self.note = note.strip()

    def to_dict(self):
        """Converts the Expense object to a dictionary for saving to JSON."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an Expense object from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            note=data.get("note", ""),
            expense_id=data.get("id", 0)
        )

    def __str__(self):
        return f"[{self.date}] ID {self.id}: {self.category} - Rs. {self.amount:.2f} ({self.note})"
