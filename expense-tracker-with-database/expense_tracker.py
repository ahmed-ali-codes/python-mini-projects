import sqlite3
import pandas as pd
from datetime import datetime
import os

class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        """Initialize the expense tracker and connect to the SQLite database."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the expenses table if it does not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_expense(self, date, category, description, amount):
        """Add a new expense record."""
        try:
            # Validate date format
            datetime.strptime(date, '%Y-%m-%d')
            self.cursor.execute('''
                INSERT INTO expenses (date, category, description, amount)
                VALUES (?, ?, ?, ?)
            ''', (date, category, description, amount))
            self.conn.commit()
            print("Expense added successfully.")
        except ValueError:
            print("Incorrect date format, should be YYYY-MM-DD")
        except Exception as e:
            print(f"Error adding expense: {e}")

    def view_expenses(self):
        """View all expense records."""
        df = pd.read_sql_query("SELECT * FROM expenses", self.conn)
        if df.empty:
            print("No expenses found.")
        else:
            print(df.to_string(index=False))

    def update_expense(self, expense_id, date=None, category=None, description=None, amount=None):
        """Update an existing expense record."""
        updates = []
        params = []
        
        if date:
            updates.append("date = ?")
            params.append(date)
        if category:
            updates.append("category = ?")
            params.append(category)
        if description:
            updates.append("description = ?")
            params.append(description)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        
        if not updates:
            print("No fields to update.")
            return

        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, tuple(params))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("Expense updated successfully.")
            else:
                print("Expense ID not found.")
        except Exception as e:
            print(f"Error updating expense: {e}")

    def delete_expense(self, expense_id):
        """Delete an expense record by ID."""
        try:
            self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("Expense deleted successfully.")
            else:
                print("Expense ID not found.")
        except Exception as e:
            print(f"Error deleting expense: {e}")

    def generate_monthly_report(self, year, month):
        """Generate a summary report for a specific month and year."""
        month_str = f"{year}-{month:02d}"
        query = "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ?"
        df = pd.read_sql_query(query, self.conn, params=(month_str,))
        
        if df.empty:
            print(f"No expenses found for {month_str}.")
            return
            
        print(f"\n--- Monthly Report: {month_str} ---")
        print(df.to_string(index=False))
        
        print("\n--- Summary by Category ---")
        summary = df.groupby('category')['amount'].sum().reset_index()
        print(summary.to_string(index=False))
        
        total_expense = df['amount'].sum()
        print(f"\nTotal Expenses: ${total_expense:.2f}")

    def export_to_csv(self, filename="expenses_export.csv"):
        """Export all expenses to a CSV file."""
        df = pd.read_sql_query("SELECT * FROM expenses", self.conn)
        if df.empty:
            print("No data to export.")
            return
        try:
            df.to_csv(filename, index=False)
            print(f"Data exported successfully to {filename}.")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def close(self):
        """Close the database connection."""
        self.conn.close()

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n" + "="*30)
        print("Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Generate Monthly Report")
        print("6. Export to CSV")
        print("7. Exit")
        print("="*30)
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ")
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            category = input("Enter category (e.g., Food, Transport, Utilities): ")
            description = input("Enter description: ")
            try:
                amount = float(input("Enter amount: "))
                tracker.add_expense(date, category, description, amount)
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
                
        elif choice == '2':
            tracker.view_expenses()
            
        elif choice == '3':
            try:
                expense_id = int(input("Enter expense ID to update: "))
                print("Enter new values (leave blank to keep current):")
                date = input("New date (YYYY-MM-DD): ")
                category = input("New category: ")
                description = input("New description: ")
                amount_str = input("New amount: ")
                
                amount = float(amount_str) if amount_str else None
                date = date if date else None
                category = category if category else None
                description = description if description else None
                
                tracker.update_expense(expense_id, date, category, description, amount)
            except ValueError:
                print("Invalid input. IDs and amounts must be numeric.")
                
        elif choice == '4':
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                tracker.delete_expense(expense_id)
            except ValueError:
                print("Invalid ID. Must be numeric.")
                
        elif choice == '5':
            try:
                year = int(input("Enter year (YYYY): "))
                month = int(input("Enter month (MM): "))
                tracker.generate_monthly_report(year, month)
            except ValueError:
                print("Invalid input. Year and month must be numeric.")
                
        elif choice == '6':
            filename = input("Enter filename (default: expenses_export.csv): ")
            if not filename:
                tracker.export_to_csv()
            else:
                tracker.export_to_csv(filename)
                
        elif choice == '7':
            tracker.close()
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
