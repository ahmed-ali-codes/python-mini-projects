# 🐍 Python Projects

A growing collection of Python projects built during university coursework and personal learning. Each project is self-contained with its own source files, dependencies, and documentation — ranging from simulations to data-driven tools.

---

## Projects

| # | Project | Description | Key Libraries |
|---|---|---|---|
| 1 | [Adventure Time Theme Park Simulator](./theme-park-simulator/) | Animated theme park simulation with patron AI, ride mechanics, and real-time Matplotlib visualization | `matplotlib` |

> More projects coming soon — see the [Roadmap](#roadmap) below.

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

## Roadmap

Projects planned to be added:

- [ ] **Student Grade Manager** — store, update, and report student grades with file persistence
- [ ] **To-Do List CLI** — command-line task manager with priorities and deadlines
- [ ] **Web Scraper** — scrape and export structured data from a website using `requests` + `BeautifulSoup`
- [ ] **Number Guessing Game** — binary search-based guessing game with difficulty levels
- [ ] **Data Analyser** — read a CSV dataset, compute statistics, and plot charts with `pandas` + `matplotlib`
- [ ] **Expense Tracker** — log and categorise personal expenses, export monthly summaries to CSV

---

## Author

**Ahmed Ali** — Computer Science student building projects across Python, C, and Assembly.

---

## License

This repository is open-source under the [MIT License](./LICENSE).
