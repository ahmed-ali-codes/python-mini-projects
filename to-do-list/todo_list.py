import os

FILE_NAME = "tasks.txt"

def load_tasks():
    """Load tasks from the text file."""
    tasks = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            tasks = [line.strip() for line in file.readlines()]
    return tasks

def save_tasks(tasks):
    """Save tasks to the text file."""
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def view_tasks(tasks):
    """Display the current list of tasks."""
    if not tasks:
        print("\nYour to-do list is empty.\n")
    else:
        print("\nYour Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        print()

def add_task(tasks):
    """Prompt the user to add a new task."""
    task = input("\nEnter a new task: ").strip()
    if task:
        tasks.append(task)
        save_tasks(tasks)
        print(f"Task '{task}' added successfully!\n")
    else:
        print("Task cannot be empty.\n")

def delete_task(tasks):
    """Prompt the user to delete an existing task."""
    view_tasks(tasks)
    if tasks:
        try:
            task_num = int(input("Enter the number of the task to delete: "))
            if 1 <= task_num <= len(tasks):
                removed_task = tasks.pop(task_num - 1)
                save_tasks(tasks)
                print(f"Task '{removed_task}' deleted successfully!\n")
            else:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.\n")

def main():
    """Main loop for the To-Do List Application."""
    tasks = load_tasks()
    
    while True:
        print("=== To-Do List Menu ===")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Delete a task")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
