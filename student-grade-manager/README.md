# Student Grade Manager

A Python-based command-line application designed to efficiently manage student grades. This tool allows educators or students to store, update, and report grades with automatic file persistence, ensuring data is saved across sessions.

## Features

- **Unique Student IDs**: Each student is assigned a unique, auto-generated ID so multiple students can share the same name without conflicts.
- **Add/Edit/Delete Students**: Manage student profiles, including renaming or completely removing a student from the records using their ID.
- **Update/Delete Grades**: Assign, modify, or remove grades for specific subjects using the student's ID.
- **View Individual Grades**: Generate a grade report for a specific student, including their current average.
- **View All Grades**: Generate a comprehensive report of all students and their respective subject grades and averages.
- **Data Persistence**: Automatically saves and loads data to and from a local JSON file (`grades.json`), so you never lose your records.

## Prerequisites

- Python 3.x installed on your system.

## Installation

1. Clone the repository or download the source code:
   ```bash
   git clone <repository_url>
   cd student-graade-manager
   ```

2. No external dependencies or libraries are required as the project uses Python's built-in modules (`json`, `os`).

## Usage

1. Open your terminal or command prompt.
2. Navigate to the project directory.
3. Run the script:
   ```bash
   python grade_manager.py
   ```

### Navigation Menu
Once the application starts, you'll be greeted with an interactive menu:

```
=== Student Grade Manager ===
1. Add Student
2. Edit Student Name
3. Delete Student
4. Add/Update Grade
5. Delete Grade
6. View Student Grades
7. View All Grades
8. Exit
```

Simply input the number corresponding to the action you wish to perform and follow the on-screen prompts.

## Data Storage

All data is stored locally in a file named `grades.json` within the same directory as the script. You can manually inspect or backup this file if necessary.

## License

This project is open-source and available under the MIT License.
