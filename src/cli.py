"""
cli.py
Presentation layer providing an interactive, user-friendly, menu-driven
terminal interface for PySpend.
"""

from datetime import datetime
import sys
from typing import List

from src.analytics import FinancialAnalytics
from src.manager import ExpenseManager
from src.models import Transaction, ValidationError
from src.validators import (
    validate_category_name,
    validate_date_string,
    validate_menu_choice,
    validate_positive_amount,
)


class CLIController:
    """
    Handles terminal user interaction, prompts, table formatting, and menus.
    """
    def __init__(self, manager: ExpenseManager = None):
        self.manager = manager if manager else ExpenseManager()

    def print_header(self) -> None:
        print("\n" + "=" * 64)
        print("     SMART STUDENT EXPENSE & BUDGET TRACKER (PySpend)     ")
        print("=" * 64)

    def print_menu(self) -> None:
        print("\n--- MAIN MENU ---")
        print("[1] Log New Expense")
        print("[2] Log New Income (Allowance/Stipend)")
        print("[3] View All Transactions")
        print("[4] Filter Transactions (by Category / Month)")
        print("[5] Configure Category Monthly Budgets")
        print("[6] View Budget Health & Spending Alerts")
        print("[7] Financial Analytics & Visual Spending Chart")
        print("[8] Export Transactions to CSV")
        print("[9] Delete a Transaction")
        print("[0] Save & Exit Application")
        print("-" * 64)

    def run(self) -> None:
        """Main application lifecycle loop."""
        self.print_header()
        print("Welcome! Tracking your pocket money and student expenses made simple.")

        while True:
            try:
                self.print_menu()
                choice_raw = input("Enter your choice (0-9): ").strip()
                try:
                    choice = validate_menu_choice(choice_raw, 0, 9)
                except ValidationError as ve:
                    print(f"\n[!] Input Error: {ve}")
                    continue

                if choice == 1:
                    self.handle_add_transaction("EXPENSE")
                elif choice == 2:
                    self.handle_add_transaction("INCOME")
                elif choice == 3:
                    self.handle_view_all()
                elif choice == 4:
                    self.handle_filter_transactions()
                elif choice == 5:
                    self.handle_set_budget()
                elif choice == 6:
                    self.handle_view_budget_health()
                elif choice == 7:
                    self.handle_analytics_view()
                elif choice == 8:
                    self.handle_export_csv()
                elif choice == 9:
                    self.handle_delete_transaction()
                elif choice == 0:
                    self.manager.save()
                    print("\n[✓] All data successfully saved. Happy studying and smart spending!")
                    break

            except (KeyboardInterrupt, EOFError):
                print("\n\n[!] Operation interrupted by user. Saving data safely...")
                self.manager.save()
                print("[✓] State preserved. Exiting.")
                sys.exit(0)

    # ------------------ Action Handlers ------------------ #

    def handle_add_transaction(self, tx_type: str) -> None:
        print(f"\n--- Log New {tx_type.title()} ---")
        try:
            amt_str = input("Enter amount in ₹ (e.g. 250.00): ")
            amount = validate_positive_amount(amt_str)

            print("Common Categories: Food, Academics, Travel, Entertainment, Utilities, Allowance")
            cat_str = input("Enter category name: ")
            category = validate_category_name(cat_str)

            date_prompt = f"Enter date (YYYY-MM-DD) or press [Enter] for today ({datetime.now().strftime('%Y-%m-%d')}): "
            date_raw = input(date_prompt)
            date_str = validate_date_string(date_raw)

            note = input("Enter optional note/description (e.g. Lunch with friends): ").strip()

            tx, alert = self.manager.add_transaction(
                amount=amount,
                category=category,
                tx_type=tx_type,
                date_str=date_str,
                note=note
            )

            print(f"\n[✓] Success: Added {tx_type} {tx.id} for ₹{tx.amount:.2f} under '{tx.category}'.")

            # Inline threshold warning check
            if alert:
                status = alert["status"]
                badge = alert["badge"]
                spent = alert["spent"]
                limit = alert["monthly_limit"]
                pct = alert["utilization_pct"]
                print(f"\n>>> BUDGET NOTICE {badge} <<<")
                print(f"    You have spent ₹{spent:,.2f} of your ₹{limit:,.2f} budget for '{category}' ({pct}% utilized)!")

        except ValidationError as ve:
            print(f"\n[X] Validation Error: {ve}")

    def handle_view_all(self) -> None:
        txs = self.manager.get_all_transactions()
        self.render_transaction_table(txs, title="ALL TRANSACTIONS")

    def handle_filter_transactions(self) -> None:
        print("\n--- Filter Transactions ---")
        print("[1] Filter by Category")
        print("[2] Filter by Month (1-12)")
        print("[3] Filter by Type (Expense / Income)")
        choice = input("Select filter mode (1-3): ").strip()

        if choice == "1":
            cat = input("Enter category name to filter (e.g. Food): ").strip()
            txs = self.manager.filter_transactions(category=cat)
            self.render_transaction_table(txs, title=f"TRANSACTIONS IN '{cat.title()}'")
        elif choice == "2":
            m_str = input("Enter month number (1-12): ").strip()
            if m_str.isdigit() and 1 <= int(m_str) <= 12:
                txs = self.manager.filter_transactions(month=int(m_str))
                self.render_transaction_table(txs, title=f"TRANSACTIONS FOR MONTH {int(m_str):02d}")
            else:
                print("[!] Invalid month number.")
        elif choice == "3":
            t_str = input("Enter type (EXPENSE or INCOME): ").strip().upper()
            if t_str in ("EXPENSE", "INCOME"):
                txs = self.manager.filter_transactions(tx_type=t_str)
                self.render_transaction_table(txs, title=f"ALL {t_str} TRANSACTIONS")
            else:
                print("[!] Invalid type. Must be EXPENSE or INCOME.")
        else:
            print("[!] Invalid choice.")

    def handle_set_budget(self) -> None:
        print("\n--- Configure Category Monthly Budget ---")
        try:
            cat_str = input("Enter category name (e.g. Food, Travel): ")
            category = validate_category_name(cat_str)

            amt_str = input(f"Enter monthly spending limit for '{category}' in ₹: ")
            limit = validate_positive_amount(amt_str)

            b = self.manager.set_budget(category, limit)
            print(f"\n[✓] Budget updated: '{b.category}' monthly cap set to ₹{b.monthly_limit:,.2f}.")
        except ValidationError as ve:
            print(f"\n[X] Error: {ve}")

    def handle_view_budget_health(self) -> None:
        print("\n" + "=" * 80)
        print("                         MONTHLY BUDGET HEALTH CHECK                           ")
        print("=" * 80)
        reports = self.manager.get_all_budgets_health()
        if not reports:
            print("  No category budgets have been configured yet.")
            return

        print(f"{'Category':<14} {'Budget Limit':<14} {'Spent':<14} {'Remaining':<14} {'Used %':<10} {'Status'}")
        print("-" * 80)

        for item in reports:
            cat = item["category"]
            limit = f"₹{item['monthly_limit']:,.2f}"
            spent = f"₹{item['spent']:,.2f}"
            rem = f"₹{item['remaining']:,.2f}"
            pct = f"{item['utilization_pct']:.1f}%"
            badge = item["badge"]
            print(f"{cat:<14} {limit:<14} {spent:<14} {rem:<14} {pct:<10} {badge}")

        print("-" * 80)

    def handle_analytics_view(self) -> None:
        txs = self.manager.get_all_transactions()
        totals = FinancialAnalytics.compute_totals(txs)
        breakdown = FinancialAnalytics.category_breakdown(txs)
        top_cat, top_amt = FinancialAnalytics.get_highest_spending_category(txs)

        print("\n" + "=" * 70)
        print("                   FINANCIAL SUMMARY & INSIGHTS                       ")
        print("=" * 70)
        print(f"  Total Recorded Income    : ₹{totals['total_income']:,.2f}")
        print(f"  Total Recorded Expenses  : ₹{totals['total_expense']:,.2f}")
        print(f"  Net Savings / Balance    : ₹{totals['net_savings']:,.2f}")
        print(f"  Overall Savings Rate     : {totals['savings_rate']:.1f}%")
        print(f"  Top Spending Category    : {top_cat} (₹{top_amt:,.2f})")
        print("-" * 70)
        print("Category-Wise Expense Distribution:")
        print(FinancialAnalytics.generate_ascii_bar_chart(breakdown, bar_width=25))
        print("=" * 70)

    def handle_export_csv(self) -> None:
        try:
            path_str = self.manager.export_csv()
            print(f"\n[✓] Transactions exported successfully to:\n    {path_str}")
        except Exception as err:
            print(f"\n[X] Export Failed: {err}")

    def handle_delete_transaction(self) -> None:
        tx_id = input("\nEnter transaction ID to delete (e.g. tx_001): ").strip()
        tx = self.manager.get_transaction(tx_id)
        if not tx:
            print(f"[!] No transaction found with ID '{tx_id}'.")
            return

        confirm = input(f"Are you sure you want to delete '{tx}'? (y/N): ").strip().lower()
        if confirm == 'y':
            if self.manager.delete_transaction(tx_id):
                print(f"[✓] Transaction {tx_id} deleted successfully.")
            else:
                print("[!] Failed to delete transaction.")
        else:
            print("Deletion canceled.")

    def render_transaction_table(self, transactions: List[Transaction], title: str = "TRANSACTIONS") -> None:
        """Renders an aligned ASCII table of transactions."""
        print("\n" + "=" * 88)
        print(f"                               {title} ({len(transactions)} Records)")
        print("=" * 88)
        if not transactions:
            print("  No transactions found.")
            print("=" * 88)
            return

        print(f"{'ID':<10} {'Date':<12} {'Type':<9} {'Category':<15} {'Amount (₹)':>12}  {'Note'}")
        print("-" * 88)
        for tx in transactions:
            type_symbol = "-" if tx.type == "EXPENSE" else "+"
            amt_str = f"{type_symbol}₹{tx.amount:,.2f}"
            print(f"{tx.id:<10} {tx.date_str:<12} {tx.type:<9} {tx.category:<15} {amt_str:>12}  {tx.note}")
        print("=" * 88)
