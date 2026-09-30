"""
storage.py
Handles persistent storage of transactions and budget configurations in JSON format,
as well as exporting transaction history to standard CSV spreadsheets.
"""

import csv
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from src.models import Budget, ExpenseTrackerError, Transaction


class StorageHandler:
    """
    Manages local file I/O operations for data persistence and export.
    """
    def __init__(self, data_dir: str = "data", filename: str = "expenses.json"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.data_dir / filename

    def load_data(self) -> Tuple[List[Transaction], Dict[str, Budget]]:
        """
        Reads and parses the JSON storage file.
        Returns a tuple of (transactions_list, budgets_dict).
        If the file does not exist or is empty, returns empty structures.
        If the file is corrupted, creates a backup and resets gracefully.
        """
        if not self.filepath.exists():
            return [], {}

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return [], {}
                data = json.loads(content)

            transactions = [
                Transaction.from_dict(tx_dict) 
                for tx_dict in data.get("transactions", [])
            ]
            budgets = {
                cat: Budget.from_dict(b_dict)
                for cat, b_dict in data.get("budgets", {}).items()
            }
            return transactions, budgets

        except (json.JSONDecodeError, KeyError, Exception) as err:
            # Automatic corruption recovery: backup corrupted file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.data_dir / f"expenses_corrupt_backup_{timestamp}.json"
            try:
                if self.filepath.exists():
                    os.replace(self.filepath, backup_path)
            except OSError:
                pass
            print(f"\n[!] Warning: Data file was damaged ({err}). Backed up to '{backup_path.name}'. Starting with fresh data.")
            return [], {}

    def save_data(self, transactions: List[Transaction], budgets: Dict[str, Budget]) -> bool:
        """
        Saves the current state of transactions and budgets to JSON.
        Uses safe write pattern to prevent data loss.
        """
        data = {
            "transactions": [tx.to_dict() for tx in transactions],
            "budgets": {cat: b.to_dict() for cat, b in budgets.items()},
            "last_updated": datetime.now().isoformat()
        }

        temp_path = self.filepath.with_suffix(".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, self.filepath)
            return True
        except Exception as err:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass
            raise ExpenseTrackerError(f"Failed to persist data: {err}")

    def export_to_csv(self, transactions: List[Transaction], export_filename: str = "expenses_export.csv") -> Path:
        """
        Exports all transactions to a structured CSV file.
        """
        export_path = self.data_dir / export_filename
        fieldnames = ["ID", "Date", "Type", "Category", "Amount (INR)", "Note"]

        try:
            with open(export_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for tx in transactions:
                    writer.writerow({
                        "ID": tx.id,
                        "Date": tx.date_str,
                        "Type": tx.type,
                        "Category": tx.category,
                        "Amount (INR)": f"{tx.amount:.2f}",
                        "Note": tx.note
                    })
            return export_path
        except Exception as err:
            raise ExpenseTrackerError(f"Failed to export CSV: {err}")
