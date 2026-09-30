"""
main.py
Main entry point: Runs a simple interactive menu for tracking student expenses.
"""

import os
import sys

# Ensure project root is available on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import Expense
from src.storage import load_expenses, save_expenses
from src.tracker import ExpenseTracker


def print_menu():
    print("\n" + "=" * 45)
    print("      STUDENT EXPENSE TRACKER")
    print("=" * 45)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. View Category Summary")
    print("4. Check Monthly Budget Status")
    print("5. Set Monthly Budget")
    print("6. Save and Exit")
    print("-" * 45)


def main():
    expenses = load_expenses()
    tracker = ExpenseTracker(expenses=expenses, monthly_budget=5000.0)
    print(f"\nWelcome! Loaded {len(tracker.expenses)} saved expenses.")

    while True:
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            try:
                amount_input = input("Enter amount (Rs.): ").strip()
                amount = float(amount_input)
                if amount <= 0:
                    print("[Error] Amount must be greater than zero.")
                    continue

                category = input("Enter category (e.g. Food, Books, Travel): ").strip()
                if not category:
                    category = "General"

                date = input("Enter date (YYYY-MM-DD): ").strip()
                note = input("Enter note (optional): ").strip()

                exp = tracker.add_expense(amount, category, date, note)
                save_expenses(tracker.expenses)
                print(f"[OK] Added Expense #{exp.id}: Rs. {exp.amount:.2f} for '{exp.category}'")

                # Budget check alert
                b_status = tracker.check_budget_status()
                if b_status["status"] == "WARNING":
                    print(f"[!] Warning: You have reached {b_status['percent_used']}% of your monthly budget!")
                elif b_status["status"] == "EXCEEDED":
                    print(f"[!] Alert: Budget exceeded by Rs. {abs(b_status['remaining']):.2f}!")

            except ValueError:
                print("[Error] Invalid amount! Please enter numeric digits.")

        elif choice == "2":
            print("\n--- ALL EXPENSES ---")
            if not tracker.expenses:
                print("No expenses recorded yet.")
            else:
                print(f"{'ID':<4} {'Date':<12} {'Category':<14} {'Amount':>10}  {'Note'}")
                print("-" * 55)
                for exp in tracker.expenses:
                    print(f"{exp.id:<4} {exp.date:<12} {exp.category:<14} Rs. {exp.amount:>7.2f}  {exp.note}")
                print("-" * 55)
                print(f"Total Spent: Rs. {tracker.get_total_expenses():.2f}")

        elif choice == "3":
            print("\n--- CATEGORY BREAKDOWN ---")
            totals = tracker.get_category_totals()
            if not totals:
                print("No expenses to summarize.")
            else:
                for cat, total in sorted(totals.items()):
                    print(f"  {cat:<15}: Rs. {total:.2f}")
                print(f"  {'TOTAL':<15}: Rs. {tracker.get_total_expenses():.2f}")

        elif choice == "4":
            b_status = tracker.check_budget_status()
            print("\n--- BUDGET STATUS ---")
            print(f"  Monthly Budget : Rs. {b_status['budget']:.2f}")
            print(f"  Total Spent    : Rs. {b_status['spent']:.2f}")
            print(f"  Remaining      : Rs. {b_status['remaining']:.2f}")
            print(f"  Budget Used    : {b_status['percent_used']}%")
            print(f"  Status         : [{b_status['status']}]")

        elif choice == "5":
            try:
                new_budget_str = input("Enter new monthly budget in Rs.: ").strip()
                new_budget = float(new_budget_str)
                if new_budget <= 0:
                    print("[Error] Budget must be greater than zero.")
                    continue
                tracker.monthly_budget = new_budget
                print(f"[OK] Monthly budget updated to Rs. {tracker.monthly_budget:.2f}")
            except ValueError:
                print("[Error] Please enter a valid number.")

        elif choice == "6":
            save_expenses(tracker.expenses)
            print("Expenses saved successfully. Goodbye!")
            break

        else:
            print("[Error] Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
