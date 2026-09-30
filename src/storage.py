"""
storage.py
Handles saving and loading expense data to/from a local JSON file.
"""

import json
import os
from src.models import Expense

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "expenses.json")

def load_expenses(filepath=DATA_FILE):
    """Loads expenses from a JSON file and returns a list of Expense objects."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Expense.from_dict(item) for item in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_expenses(expenses, filepath=DATA_FILE):
    """Saves a list of Expense objects to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        data = [exp.to_dict() for exp in expenses]
        json.dump(data, f, indent=4)
