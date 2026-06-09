# Web Scraping & Data Dashboard

A professional, modular Python CLI tool that scrapes data from multiple websites, stores it in a SQLite database, and visualizes trends through an interactive dashboard.

## 🚀 Features

- **Multi-source Scraping**:
  - **Hacker News**: Extracts top stories, scores, and comment counts.
  - **CoinGecko API**: Fetches real-time top cryptocurrency prices, market caps, and 24h changes.
  - **GitHub Trending**: Scrapes trending repositories, languages, and star counts.
- **SQLite Database**: Automatically structures and stores all scraped data for persistence and analysis.
- **Data Visualization**: Generates a beautiful, multi-panel dark-themed dashboard using Matplotlib and Pandas.
- **Modular Design**: Easy to extend with new scrapers by inheriting from the `BaseScraper` class.

## 🛠️ Built With

- **Python 3**
- [Requests](https://pypi.org/project/requests/) - For HTTP requests and API calls
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - For HTML parsing
- [Pandas](https://pandas.pydata.org/) - For data manipulation
- [Matplotlib](https://matplotlib.org/) - For chart generation
- **SQLite3** - For data storage (built into Python)

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scrapping-and-data-dashboard.git
   cd web-scrapping-and-data-dashboard
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

The tool provides a simple CLI interface through `main.py`.

### 1. Run Everything (Scrape & Dashboard)
This is the easiest way to see the tool in action. It runs all scrapers and generates the dashboard.
```bash
python main.py all
```

### 2. Run Only Scrapers
Scrape all sources and update the database without generating the dashboard:
```bash
python main.py scrape
```

You can also run a specific scraper:
```bash
python main.py scrape --source hackernews
python main.py scrape --source crypto
python main.py scrape --source github
```

### 3. Generate Dashboard Only
Generate the dashboard from existing data in the database:
```bash
python main.py dashboard
```

## 📊 Dashboard Output

The generated dashboard will be saved as a high-resolution PNG image at:
`output/dashboard.png`

It includes:
1. Top Hacker News Stories by Score (Horizontal Bar Chart)
2. Top Cryptocurrencies by Price (Log-Scale Bar Chart)
3. Cryptocurrency 24h Price Change (Colored Bar Chart)
4. Trending Languages on GitHub (Donut/Pie Chart)

## 📁 Project Structure

```text
web-scrapping-and-data-dashboard/
├── config.py                  # Global configurations and URLs
├── main.py                    # CLI entry point
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
├── database/
│   └── db_manager.py          # SQLite database connection and operations
├── scrapers/
│   ├── base_scraper.py        # Abstract base class for scrapers
│   ├── hackernews_scraper.py  # BS4 scraper for Hacker News
│   ├── crypto_scraper.py      # API scraper for CoinGecko
│   └── github_scraper.py      # BS4 scraper for GitHub Trending
├── dashboard/
│   └── visualizer.py          # Matplotlib chart generation logic
└── output/                    # Directory for generated dashboard images
```

## 📝 License

This project is licensed under the MIT License.
