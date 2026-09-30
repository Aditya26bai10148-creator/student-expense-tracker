# Student Expense Tracker

A simple, lightweight Python CLI application to help students log daily expenses, monitor category spending, and track monthly budgets.

---

## Features
- **Add Expenses**: Log date, category, amount, and an optional note.
- **View All Expenses**: See a clean table of all past expenses and the total sum.
- **Category Summary**: See how much money was spent on Food, Books, Travel, etc.
- **Monthly Budget Check**: Set a monthly budget and get alerts if spending crosses 80% or exceeds 100%.
- **Automatic Storage**: All records are saved to `data/expenses.json` automatically.

---

## Technologies Used
- **Language**: Python 3.10+
- **Modules**: Standard library only (`json`, `os`, `sys`, `unittest`) — no external packages required!

---

## Project Structure
```text
student-expense-tracker/
├── data/
│   └── expenses.json       # Saved expenses data
├── src/
│   ├── __init__.py
│   ├── models.py           # Expense class definition
│   ├── tracker.py          # Calculation and tracking logic
│   ├── storage.py          # JSON save and load functions
│   └── main.py             # Interactive menu CLI
├── tests/
│   ├── __init__.py
│   └── test_tracker.py     # Unit test cases
├── README.md               # Project documentation
├── statement.md            # Problem statement and scope
└── PROJECT_REPORT.md       # Project report for submission
```

---

## How to Run

1. Clone or download this repository.
2. Open terminal in the project folder.
3. Run the application:
```bash
python3 src/main.py
```

---

## How to Run Tests

To verify that the tracking and budget logic work as expected:
```bash
python3 -m unittest discover -s tests -v
```

All 5 unit tests should pass with `OK`.

---

## Sample Preview

```text
=============================================
      STUDENT EXPENSE TRACKER
=============================================
1. Add New Expense
2. View All Expenses
3. View Category Summary
4. Check Monthly Budget Status
5. Set Monthly Budget
6. Save and Exit
---------------------------------------------
Enter choice (1-6): 4

--- BUDGET STATUS ---
  Monthly Budget : Rs. 5000.00
  Total Spent    : Rs. 4540.00
  Remaining      : Rs. 460.00
  Budget Used    : 90.8%
  Status         : [WARNING]
```

---

## Author
- **Name**: Aditya Vardhan
- **Course**: Introduction to Programming in Python
- **Institution**: Vellore Institute of Technology (VIT)
