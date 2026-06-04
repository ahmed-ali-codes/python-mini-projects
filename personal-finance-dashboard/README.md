# Personal Finance Dashboard

A Python-based data analysis and visualization tool that reads bank transactions from a CSV file, calculates spending by category, and displays informative charts.

## Features

- **Data Ingestion**: Reads financial transactions from a CSV file.
- **Data Analysis**: Uses `pandas` to group and calculate total spending per category.
- **Data Visualization**: Uses `matplotlib` to generate interactive Bar and Pie charts for a clear visual breakdown of your finances.

## Prerequisites

Make sure you have Python installed. You will need to install the required libraries:

```bash
pip install pandas matplotlib
```

## Usage

1. **Prepare Data**: Ensure you have a `transactions.csv` file in the same directory as the script. The CSV must have at least `Category` and `Amount` columns. A sample is provided.
2. **Run the Script**: 
   ```bash
   python dashboard.py
   ```
3. **View Results**: The script will print the summarized data to the console and open a window with the charts.

## Example CSV Format (`transactions.csv`)

```csv
Date,Description,Category,Amount
2023-10-01,Grocery Store,Food,150.50
2023-10-02,Gas Station,Transport,45.00
2023-10-04,Internet Provider,Utilities,80.00
```
