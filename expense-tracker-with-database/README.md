# Expense Tracker with Database

A Python-based command-line application that allows you to manage and track your expenses. Data is securely stored using a local SQLite database, and reports can be generated and exported to CSV using `pandas`.

## Features
- **SQLite Database Integration:** Expenses are saved persistently using SQLite.
- **Object-Oriented Programming (OOP):** The application relies on an `ExpenseTracker` class for clean organization and structure.
- **CRUD Operations:** Create, Read, Update, and Delete expenses effortlessly.
- **Categorization:** Classify transactions (e.g., Food, Transport, Utilities).
- **Monthly Reports:** Generate detailed monthly breakdowns that summarize expenses by category.
- **Data Export:** Export all of your tracked expenses into a CSV file for further analysis in Excel or other spreadsheet tools.

## Prerequisites
- Python 3.7+
- `pandas` library

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd expense-tracker-with-database
   ```

2. **Install requirements:**
   You will need to install the `pandas` library if you do not already have it:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program from the terminal:

```bash
python expense_tracker.py
```

### Menu Options:
1. **Add Expense:** Add a new transaction by entering the date, category, description, and amount.
2. **View All Expenses:** Display a table of all expenses currently in the database.
3. **Update Expense:** Edit an existing expense using its ID.
4. **Delete Expense:** Remove a mistakenly added expense via its ID.
5. **Generate Monthly Report:** Input a year and month to see a summary of expenses by category for that month.
6. **Export to CSV:** Export the entire database of expenses to a CSV file.
7. **Exit:** Safely close the database connection and exit the application.

## Technologies Used
- Python 3
- `sqlite3` (Standard Library)
- `pandas`
