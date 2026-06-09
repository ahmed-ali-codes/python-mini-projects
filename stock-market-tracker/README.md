# 📈 Stock Market Tracker

A feature-rich CLI tool to track stocks, monitor price alerts, and visualise historical data — powered by Yahoo Finance, pandas, matplotlib, and schedule.

## Features

| Feature | Description |
|---|---|
| 📊 Live prices | Fetch real-time prices for all watchlist tickers |
| ➕ Watchlist | Add / remove ticker symbols (persisted to `watchlist.json`) |
| 📉 Historical charts | Dark-themed price charts with MA-7, MA-20 & volume bars |
| 🔀 Comparison charts | Normalised multi-ticker overlay chart |
| 🔔 Price alerts | Set above/below thresholds — fired to console with timestamp |
| ⏱️ Scheduler | Automated price checks every minute via `schedule` |
| 🔎 Fundamentals | View sector, market cap, P/E, 52-week range |

## Data Source

Uses **[yfinance](https://github.com/ranaroussi/yfinance)** — a free Yahoo Finance wrapper. No API key required.

## Setup

```bash
# 1. Navigate to the project
cd stock-market-tracker

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

## Usage

```
[1] View watchlist prices
[2] Add ticker to watchlist
[3] Remove ticker from watchlist
[4] Plot historical chart
[5] Compare tickers chart
[6] Manage price alerts
[7] Start price monitor (scheduler)
[8] Ticker info & fundamentals
[9] Exit
```

### Example Workflow

1. **Add tickers**: Choose option `2` → enter `AAPL`, repeat for `MSFT`, `TSLA`
2. **View prices**: Choose option `1` to see live prices for all watched tickers
3. **Plot chart**: Choose option `4` → enter `AAPL` + period `3mo` → chart saved to `charts/`
4. **Compare**: Choose option `5` → enter `AAPL,MSFT,GOOGL` + period `6mo`
5. **Set alert**: Choose option `6` → `2` → e.g. `AAPL below 180.00`
6. **Monitor**: Choose option `7` — checks prices every minute and fires alert when triggered

## File Structure

```
stock-market-tracker/
├── main.py          # CLI entry point & menu loop
├── tracker.py       # yfinance data fetching (live + historical)
├── alerts.py        # Alert rule engine & console notifications
├── plotter.py       # Matplotlib chart generation
├── config.py        # JSON persistence for watchlist & alerts
├── requirements.txt # pandas, matplotlib, schedule, yfinance
├── .gitignore       # Excludes watchlist.json, alerts.json, charts/, venv/
└── README.md        # This file
```

## Generated Files (git-ignored)

| File / Dir | Description |
|---|---|
| `watchlist.json` | Your saved ticker symbols |
| `alerts.json` | Your saved alert rules |
| `charts/` | PNG chart files output by plotter |

## Dependencies

- [`yfinance`](https://pypi.org/project/yfinance/) — Yahoo Finance data
- [`pandas`](https://pypi.org/project/pandas/) — data wrangling
- [`matplotlib`](https://pypi.org/project/matplotlib/) — chart rendering
- [`schedule`](https://pypi.org/project/schedule/) — lightweight job scheduler
