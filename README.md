# Student Expense Tracker

A simple, offline command-line tool written in Python to help students keep track of daily pocket money, canteen expenses, and monthly budget limits.

---

## Why I Built This
During college, it's very easy to spend small amounts every day—canteen snacks, tea, photocopies, travel—without realizing how quickly it all adds up. By the middle of the month, pocket money is usually gone. I built this lightweight CLI tool so I could quickly record my daily expenses in a couple of seconds right from my laptop, without dealing with slow apps, ads, or sign-ups.

---

## What It Can Do
- **Log Daily Expenses**: Save expense amounts, category names, dates, and quick notes.
- **View All Records**: Print a neat table showing all transactions and the total amount spent so far.
- **Category Summary**: Check how much money went into Food, Books, Travel, Mess, or Entertainment.
- **Budget Warnings**: Set your monthly allowance limit and get notified when you cross 80% or exceed your budget.
- **Auto-Save**: Everything gets saved into a local `data/expenses.json` file automatically.

---

## Tech Stack
- **Language**: Python 3.10+
- **Libraries**: Built using only standard Python modules (`json`, `os`, `sys`, `unittest`). No external `pip` packages needed.

---

## Project Structure
```text
student-expense-tracker/
├── data/
│   └── expenses.json       # JSON file where expenses are saved
├── src/
│   ├── __init__.py
│   ├── models.py           # Expense class definition
│   ├── tracker.py          # Logic for adding expenses and checking budget
│   ├── storage.py          # Functions to save and load data from JSON
│   └── main.py             # Terminal menu and user interaction loop
├── tests/
│   ├── __init__.py
│   └── test_tracker.py     # Unit test cases
├── README.md
├── statement.md
└── PROJECT_REPORT.md
```

---

## How to Run the App

1. Open your terminal in this folder.
2. Run the main script:
```bash
python3 src/main.py
```

### Sample Terminal Output
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

## Running the Unit Tests

To run the unit tests:
```bash
python3 -m unittest discover -s tests -v
```

All 5 tests will run and display `OK`.

---

## Author
- **Student**: Aditya Vardhan
- **Course**: Introduction to Programming in Python
- **College**: Vellore Institute of Technology (VIT)
