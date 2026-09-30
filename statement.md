# Project Statement: Smart Student Expense & Budget Tracker (PySpend)

## 1. Problem Statement
As college students, managing personal finances is often challenging. Juggling monthly allowances, semester expenses (books, course supplies, exam fees), mess/canteen bills, and personal leisure frequently leads to overspending within the first couple of weeks of a month. Existing mobile and web finance applications are frequently overburdened with advertisements, require cloud sign-ups, lack offline privacy, and fail to provide quick, lightweight expense tracking suited for student life.

There is a distinct need for a lightweight, modular, and privacy-first local CLI application built in Python that allows students to record income and expenditures, organize expenses by categories, establish monthly category-specific spending limits, and visualize spending breakdowns with warning thresholds before a budget is exceeded.

---

## 2. Scope of the Project
The scope of the **Smart Student Expense & Budget Tracker** encompasses:
- **Local Data Persistence**: Storing transaction histories and budget configurations in clean, human-readable JSON files with optional CSV export capabilities, removing external database dependencies.
- **Transaction & Category Management**: Enabling complete CRUD operations for income and expenses with automatic date timestamps, validation, and customizable categories (e.g., Food, Academics, Travel, Entertainment, Utilities).
- **Budget Monitoring & Threshold Alerts**: Allowing students to set monthly budget limits per category, computing real-time utilization percentages, and issuing warnings when spending crosses 80% or 100% of the allocated quota.
- **Analytics & Reporting**: Generating monthly summaries, category distribution statistics, and text-based visual spending charts directly in the terminal without external plotting libraries.
- **Defensive Input Handling**: Robust validation for financial amounts, date formats, and menu choices to prevent application crashes or data corruption.

### Out of Scope (for Future Iterations):
- Integration with live bank APIs or SMS scraping (for privacy and complexity reasons in an introductory Python course).
- Multi-user authentication over network sockets.
- Cloud database syncing.

---

## 3. Target Users
1. **University / College Students**: Individuals receiving fixed monthly allowances or pocket money who need an easy, distraction-free tool to avoid running out of funds before the month ends.
2. **Beginner Programmers & Evaluators**: Students and academic evaluators looking for a clean, modular, and strictly standard-library-compliant reference project demonstrating Python OOP, file I/O, error handling, and unit testing.
3. **Privacy-Conscious Individuals**: Users who prefer managing their financial data offline on their local machines rather than uploading personal expenditure data to commercial cloud services.

---

## 4. High-Level Features
- **1. Transaction Logging & Categorization**:
  - Add expense and income entries with amount, category, date, and optional notes.
  - View all transactions in a neatly formatted tabular display.
  - Filter transactions by date range, month, or category.
  - Edit or delete erroneous transaction entries by unique ID.

- **2. Dynamic Monthly Budgeting & Alert System**:
  - Set specific monthly spending caps for individual categories.
  - View real-time budget health (Spent vs. Remaining balance).
  - Visual alert triggers when spending exceeds 80% (Warning) or 100% (Exceeded).

- **3. Financial Insights & Visual Terminal Analytics**:
  - Net balance calculation (Total Income - Total Expenses).
  - Category-wise expense breakdown with percentage share.
  - Terminal-based ASCII bar charts displaying spending distribution.
  - Summary metrics highlighting the highest spending category and average daily expenditure.

- **4. File I/O & Export Subsystem**:
  - Automatic loading and saving of state in JSON format upon startup/exit.
  - Export transaction history and monthly balance sheet to standard CSV format for spreadsheet analysis.
  - Corrupted data file backup and graceful error recovery.

- **5. Interactive & Resilient Terminal UI**:
  - Clear, numbered menu-driven navigation.
  - Strict input validation with user-friendly error messages for invalid formats.
