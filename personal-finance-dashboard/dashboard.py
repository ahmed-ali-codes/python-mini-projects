import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    """Loads transactions data from a CSV file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def calculate_spending_by_category(df):
    """Calculates total spending per category."""
    if 'Category' not in df.columns or 'Amount' not in df.columns:
        print("Error: CSV must contain 'Category' and 'Amount' columns.")
        return None
    
    # Group by category and sum the amounts
    spending = df.groupby('Category')['Amount'].sum().reset_index()
    # Sort by amount descending
    spending = spending.sort_values(by='Amount', ascending=False)
    return spending

def plot_spending(spending_df):
    """Displays bar and pie charts for spending by category."""
    if spending_df is None or spending_df.empty:
        print("No data to plot.")
        return

    # Create a figure with two subplots
    plt.figure(figsize=(12, 6))
    
    # 1. Bar Chart
    plt.subplot(1, 2, 1)
    plt.bar(spending_df['Category'], spending_df['Amount'], color='skyblue', edgecolor='black')
    plt.title('Spending by Category (Bar Chart)', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 2. Pie Chart
    plt.subplot(1, 2, 2)
    plt.pie(spending_df['Amount'], labels=spending_df['Category'], autopct='%1.1f%%', 
            startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Spending Distribution (Pie Chart)', fontsize=14)
    
    # Adjust layout to prevent overlap and show plot
    plt.tight_layout()
    plt.show()

def main():
    print("=" * 40)
    print("   Personal Finance Dashboard")
    print("=" * 40)
    
    file_path = 'transactions.csv'
    
    df = load_data(file_path)
    if df is not None:
        print("\nTransactions Loaded Successfully:")
        print("-" * 40)
        print(df.head())
        print("-" * 40)
        
        spending = calculate_spending_by_category(df)
        if spending is not None:
            print("\nTotal Spending by Category:")
            print(spending.to_string(index=False))
            print("-" * 40)
            
            print("\nGenerating charts... (Close the chart window to exit)")
            plot_spending(spending)

if __name__ == "__main__":
    main()
