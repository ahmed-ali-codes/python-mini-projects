# 🐍 Python Projects

A growing collection of Python projects built during university coursework and personal learning. Each project is self-contained with its own source files, dependencies, and documentation — ranging from simulations to data-driven tools.

---

## Projects

| # | Project | Description | Key Libraries |
|---|---|---|---|
| 1 | [Adventure Time Theme Park Simulator](./theme-park-simulator/) | Animated theme park simulation with patron AI, ride mechanics, and real-time Matplotlib visualization | `matplotlib` |
| 2 | [Simple Python Calculator](./calculator/) | Command-line based simple calculator supporting basic operations | Built-in |
| 3 | [Expense Tracker](./expense-tracker/) | Command-line expense tracker demonstrating core programming concepts | Built-in |
| 4 | [Expense Tracker with Database](./expense-tracker-with-database/) | Command-line application to manage expenses securely stored using SQLite | `sqlite3`, `pandas` |
| 5 | [File Organizer](./file-organizer/) | Script to automatically organize files based on their file extensions | `os`, `shutil` |
| 6 | [Number Guessing Game](./number-guessing-game/) | Interactive command-line guessing game demonstrating core fundamentals | `random` |
| 7 | [Password Generator](./password-generator/) | Simple and secure command-line password generator with customizable length | `random`, `string` |
| 8 | [Personal Finance Dashboard](./personal-finance-dashboard/) | Data analysis and visualization tool that reads bank transactions from CSV | `pandas`, `matplotlib` |
| 9 | [Python Quiz Game](./quiz-game/) | Interactive command-line quiz game demonstrating dictionaries | Built-in |
| 10 | [Rock-Paper-Scissors](./rock-paper-scissors/) | Classic game against the computer in Best-of-3 or Best-of-5 modes | `random` |
| 11 | [Python To-Do List](./to-do-list/) | Interactive command-line To-Do List application | Built-in |
| 12 | [Python Weather App](./weather-app/) | Command-line weather application making HTTP requests and handling JSON | `requests`, `json` |
| 13 | [Student Grade Manager](./student-graade-manager/) | Command-line application to store, update, and report student grades with file persistence | `json`, `os` |

---

## How to Run Any Project

Each project folder has its own `README.md` with full setup and run instructions. The general pattern is:

```bash
# 1. Navigate into the project folder
cd project-folder-name

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the program
python3 main.py
```

> Python 3.7+ is recommended across all projects.

---

## Repository Structure

```
python-projects/
│
├── theme-park-simulator/     ← Animated theme park simulation
│   ├── adventureTime.py
│   ├── attractions.py
│   ├── theme_park.py
│   ├── patrons.py
│   ├── map1.csv / map2.csv
│   ├── para1.csv / para2.csv
│   ├── requirements.txt
│   └── README.md
│
└── README.md                 ← This file
```

---

## Concepts Covered Across Projects

- Object-oriented programming (classes, inheritance, encapsulation)
- Real-time animation and data visualization with Matplotlib
- Simulation design (state machines, agent behavior, event loops)
- File I/O and CSV parsing
- Command-line argument handling (`argparse`)
- Pathfinding and collision/barrier logic
- Modular project structure across multiple `.py` files

---

## Author

**Ahmed Ali** — Computer Science student building projects across Python, C, and Assembly.

---

## License

This repository is open-source under the [MIT License](./LICENSE).
