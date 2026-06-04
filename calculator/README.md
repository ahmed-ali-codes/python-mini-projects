# Simple Python Calculator

A command-line based simple calculator built with Python. 

## Features

- **Basic Operations:** Supports Addition, Subtraction, Multiplication, and Division.
- **Error Handling:** Robust handling for division by zero and invalid inputs (non-numeric values).
- **Interactive Menu:** Easy-to-use continuous loop to perform multiple calculations without restarting the program.

## Concepts Learned

- Defining and calling functions.
- Handling user input.
- Conditional statements (`if`, `elif`, `else`).
- Exception handling (`try`, `except`).
- Loops (`while`).

## Prerequisites

- Python 3.x installed on your system.

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the directory where the file is located.
3. Run the script using the following command:

```bash
python calculator.py
```

## Usage

When you run the script, you will see a menu of operations:

```
Welcome to the Simple Python Calculator!
Select operation:
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exit
```

1. Enter the number corresponding to the operation you want to perform.
2. Input the first and second numbers when prompted.
3. The result will be displayed on the screen.
4. You can continue calculating or choose `5` to exit the application.

## Example

```
Enter choice (1/2/3/4/5): 4
Enter first number: 10
Enter second number: 0
10.0 / 0.0 = Error: Division by zero is not allowed.
------------------------------
Enter choice (1/2/3/4/5): 1
Enter first number: 5
Enter second number: 7
5.0 + 7.0 = 12.0
------------------------------
```
