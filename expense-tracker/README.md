# Expense Tracker

A simple command-line Expense Tracker built in Python. This project demonstrates core programming concepts such as working with dictionaries and file storage using CSV files.

## Features

- **Add Expenses**: Quickly input your expenses with an item name, amount, category, and a brief description.
- **Edit Expenses**: Select any existing expense by its ID to modify its details. You can update only the fields you want and leave the rest unchanged.
- **View All Expenses**: Display a neatly formatted table showing all your recorded expenses at a glance.
- **Categorize Spending**: View a summary of your spending grouped by categories.
- **Show Total Expenses**: Calculate and display the total amount of all recorded expenses.
- **Data Persistence**: Automatically saves all expense data to an `expenses.csv` file, ensuring your records are retained between sessions.

## Concepts Applied

- **Dictionaries**: Used to structure and store individual expense records.
- **File Storage**: Utilizes Python's built-in `csv` module to seamlessly read from and write to a CSV file.
- **Data Formatting**: String formatting is used to create neat, tabular column-based outputs in the terminal.
- **Error Handling**: Handles invalid inputs gracefully (e.g., non-numeric expense amounts, invalid IDs).

## Prerequisites

- Python 3.x installed on your machine.

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory:
   ```bash
   cd expense-tracker
   ```

## Usage

Run the program using Python:

```bash
python expense_tracker.py
```

Follow the interactive on-screen menu to manage your expenses. The application will create and maintain an `expenses.csv` file in the same directory to store your data.
