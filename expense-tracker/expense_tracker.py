import csv
import os

FILENAME = "expenses.csv"

def load_expenses():
    """Load expenses from the CSV file."""
    expenses = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                except ValueError:
                    pass
    return expenses

def save_expenses(expenses):
    """Save expenses to the CSV file."""
    with open(FILENAME, mode='w', newline='') as file:
        fieldnames = ['item_name', 'amount', 'category', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

def add_expense(expenses):
    """Prompt user to add a new expense."""
    item_name = input("Enter item name: ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    category = input("Enter category (e.g., Food, Transport): ").strip().title()
    description = input("Enter description: ").strip()
    
    expense = {
        'item_name': item_name,
        'amount': amount,
        'category': category,
        'description': description
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")

def categorize_spending(expenses):
    """Calculate and display spending by category."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    categories = {}
    for expense in expenses:
        cat = expense['category']
        categories[cat] = categories.get(cat, 0) + expense['amount']
    
    print("\n--- Spending by Category ---")
    for cat, total in sorted(categories.items()):
        print(f"{cat}: ${total:.2f}")

def show_total_expenses(expenses):
    """Calculate and display total expenses."""
    total = sum(expense['amount'] for expense in expenses)
    print(f"\nTotal Expenses: ${total:.2f}")

def view_all_expenses(expenses):
    """Display all expenses in a formatted table."""
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    print(f"{'ID':<3} | {'Item Name':<15} | {'Amount':<10} | {'Category':<15} | {'Description':<20}")
    print("-" * 73)
    for i, expense in enumerate(expenses, start=1):
        item = expense.get('item_name', '')[:14]
        amount = f"${expense.get('amount', 0):.2f}"
        cat = expense.get('category', '')[:14]
        desc = expense.get('description', '')[:19]
        print(f"{i:<3} | {item:<15} | {amount:<10} | {cat:<15} | {desc:<20}")

def edit_expense(expenses):
    """Prompt user to edit an existing expense."""
    if not expenses:
        print("\nNo expenses to edit.")
        return
        
    view_all_expenses(expenses)
    
    try:
        index = int(input("\nEnter the ID of the expense to edit (0 to cancel): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
        
    if index == 0:
        return
        
    if index < 1 or index > len(expenses):
        print("Invalid ID.")
        return
        
    expense = expenses[index - 1]
    
    print("\nLeave blank to keep the current value.")
    
    new_item = input(f"Enter new item name ({expense.get('item_name', '')}): ").strip()
    if new_item:
        expense['item_name'] = new_item
        
    new_amount_str = input(f"Enter new amount ({expense.get('amount', '')}): ").strip()
    if new_amount_str:
        try:
            expense['amount'] = float(new_amount_str)
        except ValueError:
            print("Invalid amount. Change ignored.")
            
    new_cat = input(f"Enter new category ({expense.get('category', '')}): ").strip().title()
    if new_cat:
        expense['category'] = new_cat
        
    new_desc = input(f"Enter new description ({expense.get('description', '')}): ").strip()
    if new_desc:
        expense['description'] = new_desc
        
    save_expenses(expenses)
    print("Expense updated successfully.")

def main():
    expenses = load_expenses()
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. Edit Expense")
        print("3. View Spending by Category")
        print("4. Show Total Expenses")
        print("5. View All Expenses (Table)")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            edit_expense(expenses)
        elif choice == '3':
            categorize_spending(expenses)
        elif choice == '4':
            show_total_expenses(expenses)
        elif choice == '5':
            view_all_expenses(expenses)
        elif choice == '6':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
