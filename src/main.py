"""
main.py
Application entry point for Smart Student Expense & Budget Tracker (PySpend).
"""

import os
from pathlib import Path
import sys

# Ensure project root is available on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cli import CLIController
from src.manager import ExpenseManager
from src.storage import StorageHandler


def main():
    """Initializes paths, loads data store, and starts the CLI loop."""
    data_dir = PROJECT_ROOT / "data"
    storage = StorageHandler(data_dir=str(data_dir), filename="expenses.json")
    manager = ExpenseManager(storage=storage)
    cli = CLIController(manager=manager)
    cli.run()


if __name__ == "__main__":
    main()
