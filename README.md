# Smart Student Expense & Budget Tracker (PySpend)

An offline, privacy-first, modular CLI application written in Python to help college students track daily expenses, manage monthly allowances, monitor category budgets, and visualize personal finances.

---

## Overview

Managing personal finances during college is notoriously tricky. Between mess bills, books, commute, and weekend social outings, it is easy to lose track of where monthly allowances disappear. 

**Smart Student Expense & Budget Tracker (`PySpend`)** was developed as part of the *Introduction to Programming in Python* course project. It provides an intuitive, lightweight, menu-driven command-line interface (CLI) to record financial transactions, enforce category-level budget limits with automated warning thresholds, generate statistical summaries, and export data to standard CSV spreadsheets—all without requiring any third-party external libraries or internet connectivity.

---

## Features

- **Transaction Management**:
  - Add expenses and income with amount, category, date, and description.
  - View all transactions in a clean, aligned tabular format.
  - Search/filter transactions by category, month, or transaction type.
  - Modify or delete existing transactions using unique IDs.
- **Budget Monitoring & Proactive Alerts**:
  - Define category-specific monthly spending limits (e.g., Food: ₹4,000, Academics: ₹1,500).
  - Immediate terminal warnings when category spending reaches 80% (Caution) and 100% (Exceeded).
- **Statistical Analytics & ASCII Visualizations**:
  - Net balance, total income, total expenditure, and savings rate calculations.
  - Category breakdown with percentage share.
  - Pure terminal ASCII bar charts illustrating expense distribution.
- **Data Persistence & Portability**:
  - Seamless persistence using structured JSON files (`data/expenses.json`).
  - Corrupt data handling with automatic backup creation.
  - One-click export to CSV (`data/expenses_export.csv`) for Excel/Google Sheets.
- **Robust Error Handling & Validation**:
  - Defensive input parsing for currency amounts, date formats (`YYYY-MM-DD`), and choice selections.

---

## Technologies & Tools Used

- **Language**: Python 3.10+ (Standard Library only — no `pip install` required)
- **Key Modules**:
  - `json` & `csv`: File serialization and data export.
  - `datetime`: Date parsing, timestamping, and monthly filtering.
  - `pathlib` & `os`: Robust, cross-platform file and directory handling.
  - `unittest`: Automated unit and validation testing suite.
- **Version Control**: Git & GitHub
- **Design Methodology**: Object-Oriented Programming (OOP) with modular Separation of Concerns (SoC).

---

## Project Structure

```text
student-expense-tracker/
│
├── data/
│   ├── expenses.json             # Persistent application data store
│   └── expenses_export.csv       # Generated CSV export file
│
├── docs/
│   ├── diagrams/                 # UML and architecture diagrams
│   └── project_report.pdf        # Final project submission report
│
├── src/
│   ├── __init__.py               # Package marker
│   ├── models.py                 # Core domain entities (Transaction, Category, Budget)
│   ├── manager.py                # Business logic & transaction/budget coordinator
│   ├── analytics.py              # Financial analytics, calculations, and ASCII chart generator
│   ├── storage.py                # JSON persistence engine & CSV exporter
│   ├── validators.py             # Input sanitization and date/currency validation
│   ├── cli.py                    # Menu-driven user interface and presentation layer
│   └── main.py                   # Application entry point
│
├── tests/
│   ├── __init__.py               # Test package marker
│   ├── test_models.py            # Unit tests for data entities
│   ├── test_manager.py           # Unit tests for expense manager CRUD operations
│   ├── test_analytics.py         # Unit tests for financial calculations & metrics
│   └── test_storage.py           # Unit tests for file serialization and recovery
│
├── .gitignore                    # Standard Python gitignore
├── README.md                     # Project overview and run instructions
├── statement.md                  # Problem statement, scope, and target users
└── PROJECT_REPORT.md             # Complete academic submission report draft
```

---

## Installation & Setup

No third-party packages or virtual environment setups are mandatory since `PySpend` uses native Python standard libraries.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/student-expense-tracker.git
cd student-expense-tracker
```

### 2. Verify Python Version
Make sure Python 3.10 or higher is installed:
```bash
python3 --version
```

### 3. Run the Application
Start the interactive terminal CLI:
```bash
python3 -m src.main
```
*(or run directly: `python3 src/main.py`)*

---

## Sample Usage & Terminal Preview

### Main Menu
```text
============================================================
       SMART STUDENT EXPENSE & BUDGET TRACKER (PySpend)     
============================================================
[1] Log New Expense
[2] Log New Income
[3] View All Transactions
[4] Filter Transactions by Category / Month
[5] Set & Manage Monthly Category Budgets
[6] View Budget Health & Spending Alerts
[7] Financial Analytics & Category Chart
[8] Export Data to CSV
[9] Delete / Edit Transaction
[0] Save & Exit
============================================================
Enter your choice (0-9): 
```

### Budget Alert & Health Check Preview
```text
-------------------------------------------------------------------------------------
Category        Budget (₹)      Spent (₹)       Remaining (₹)   Used %    Status
-------------------------------------------------------------------------------------
Food            4000.00         3450.00         550.00          86.2%     [!] WARNING (>80%)
Academics       1500.00          620.00         880.00          41.3%     [OK] Under Budget
Travel           800.00          920.00        -120.00         115.0%     [X] EXCEEDED
Entertainment   1000.00          350.00         650.00          35.0%     [OK] Under Budget
-------------------------------------------------------------------------------------
```

### Terminal ASCII Spending Chart
```text
Category-Wise Expense Distribution:
------------------------------------------------------------
Food          | #################################### 64.6% (₹3,450.00)
Travel        | ########## 17.2% (₹920.00)
Academics     | ####### 11.6% (₹620.00)
Entertainment | #### 6.6% (₹350.00)
------------------------------------------------------------
Total Expenditure: ₹5,340.00 across 4 categories.
```

---

## Running Automated Tests

A comprehensive unit testing suite using Python's built-in `unittest` framework validates all calculations, serialization routines, and business logic:

Run all tests from the project root:
```bash
python3 -m unittest discover -s tests -v
```

Expected output:
```text
test_add_transaction (test_manager.TestExpenseManager) ... ok
test_budget_threshold_warning (test_manager.TestExpenseManager) ... ok
test_category_percentage_distribution (test_analytics.TestAnalytics) ... ok
test_invalid_amount_validation (test_models.TestModels) ... ok
test_json_save_and_reload (test_storage.TestStorage) ... ok
...
Ran 12 tests in 0.045s

OK
```

---

## Author & Academic Acknowledgement

- **Course**: Introduction to Programming in Python (Flipped Course Project)
- **Author**: Aditya Vardhan
- **Institution**: Vellore Institute of Technology (VIT)
