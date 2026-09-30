# Project Statement: Student Expense Tracker

## 1. Problem Statement
Managing daily pocket money and monthly living allowances is a major challenge for college students. Between hostel mess bills, stationery, canteen food, travel, and social outings, students often lose track of their spending and run out of money before the month ends. Existing finance apps are often filled with ads, require online account sign-ups, and have complicated interfaces. A simple, offline, menu-driven Python application helps students log daily expenses, view spending by category, and stay within their monthly budget.

## 2. Scope of the Project
- **Record Expenses**: Add daily expenses with amount, category, date, and a note.
- **Category Summary**: Group and calculate total money spent per category (e.g. Food, Books, Travel).
- **Budget Tracking**: Set a monthly budget and receive automatic warnings when 80% or 100% of the budget is spent.
- **Data Persistence**: Save and reload all expenses to a local `expenses.json` file so records are preserved across sessions.

## 3. Target Users
- College and university students who want an easy tool to track their daily allowance.
- Students and teachers looking for a clear, modular, beginner-friendly Python project.

## 4. High-Level Features
1. **Add Expense**: Record amount, category, date, and note.
2. **View Expenses**: Display all records in a formatted list with total expenditure.
3. **Category Breakdown**: View total spent in each category.
4. **Budget Alert**: Check whether spending is within limits or in warning/exceeded state.
5. **Persistent Storage**: Automatic saving and loading using Python's standard `json` module.
