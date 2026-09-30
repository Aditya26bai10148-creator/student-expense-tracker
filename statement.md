# Project Statement: Student Expense Tracker

## 1. Problem Statement
As a college student living away from home, managing monthly pocket money is always a hassle. Between eating at the campus canteen or food courts (like Foodys and Gazebo), buying printouts and lab records, paying for laundry, and weekend outings with friends, it's very easy to lose track of where the money went. Most of the time, students realize they have run out of cash only when their bank balance drops near zero before the month even ends.

Most budgeting apps on the App Store or Play Store are annoying to use for simple student needs. They ask for email logins, show pop-up ads, want you to link your bank accounts, and need a constant internet connection. I wanted to build a simple, offline command-line Python program where I can quickly type in what I spent in a few seconds, see how much I've spent on each category, and get a warning before I cross my monthly budget.

## 2. Scope of the Project
- **Logging Daily Expenses**: Easily record daily expenses with amount, category, date, and a short note.
- **Category-Wise Spending**: See total money spent across categories like Food, Books, Travel, Mess, and Entertainment.
- **Monthly Budget Check**: Set a monthly spending limit (like Rs. 5000) and get a warning if spending crosses 80% or goes over 100%.
- **File Storage**: Automatically save all entries into a local `expenses.json` file so records aren't lost when closing the terminal.

## 3. Target Users
- University and college students who want a quick, distraction-free way to track pocket money.
- Anyone looking for a lightweight, offline expense tracking script in Python.

## 4. Main Features
1. **Add an Expense**: Enter amount, category, date, and note.
2. **List All Expenses**: View all past expenses in a neat table along with the total sum.
3. **Category Breakdown**: View total money spent per category to see where most cash is going.
4. **Budget Alert System**: Instantly see if you are within safe spending limits, nearing the cap (>= 80%), or over budget (> 100%).
5. **Local JSON Saving**: All records are read and written to disk without needing any database setup.
