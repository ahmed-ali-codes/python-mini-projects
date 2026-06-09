"""
main.py — Stock Market Tracker CLI

Run with:  python main.py
"""

import sys
import time
import threading
import schedule

import config
import tracker
import alerts as alert_engine
import plotter

VALID_PERIODS = ["1wk", "1mo", "3mo", "6mo", "1y", "2y"]
CHECK_INTERVAL_MINUTES = 1


# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    import os
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 56)
    print("        📈  Stock Market Tracker  📈              ")
    print("=" * 56)


def hr():
    print("-" * 56)


def prompt(text: str) -> str:
    return input(f"  {text}: ").strip()


def pause():
    input("\n  Press Enter to continue…")


def fmt_price(price) -> str:
    return f"${price:.2f}" if price is not None else "N/A"


def fmt_mcap(val) -> str:
    if val is None:
        return "N/A"
    if val >= 1e12:
        return f"${val/1e12:.2f}T"
    if val >= 1e9:
        return f"${val/1e9:.2f}B"
    return f"${val/1e6:.2f}M"


# ─── Menu Actions ─────────────────────────────────────────────────────────────

def view_watchlist():
    hr()
    print("  📊  Watchlist — Live Prices\n")
    watchlist = config.load_watchlist()

    if not watchlist:
        print("  (Your watchlist is empty. Add a ticker first.)")
        pause()
        return

    prices = tracker.get_batch_prices(watchlist)
    print(f"  {'Ticker':<10} {'Price':>10}")
    hr()
    for ticker in watchlist:
        price = prices.get(ticker)
        print(f"  {ticker:<10} {fmt_price(price):>10}")

    pause()


def add_ticker():
    hr()
    print("  ➕  Add Ticker to Watchlist\n")
    ticker = prompt("Ticker symbol (e.g. AAPL, TSLA, MSFT)").upper()

    if not ticker:
        print("  ❌ No symbol entered.")
        pause()
        return

    print(f"  Fetching data for {ticker}…")
    price = tracker.get_current_price(ticker)

    if price is None:
        print(f"  ❌ Could not find data for '{ticker}'. Check the symbol and try again.")
        pause()
        return

    watchlist = config.load_watchlist()
    if ticker in watchlist:
        print(f"  ⚠️  '{ticker}' is already in your watchlist.")
    else:
        watchlist.append(ticker)
        config.save_watchlist(watchlist)
        print(f"  ✅ {ticker} added  (Current price: {fmt_price(price)})")

    pause()


def remove_ticker():
    hr()
    print("  🗑️  Remove Ticker from Watchlist\n")
    watchlist = config.load_watchlist()

    if not watchlist:
        print("  (Watchlist is empty.)")
        pause()
        return

    print("  Current watchlist:", ", ".join(watchlist))
    ticker = prompt("Ticker to remove").upper()

    if ticker in watchlist:
        watchlist.remove(ticker)
        config.save_watchlist(watchlist)
        print(f"  ✅ '{ticker}' removed.")
    else:
        print(f"  ❌ '{ticker}' not found in watchlist.")

    pause()


def plot_historical():
    hr()
    print("  📉  Plot Historical Chart\n")
    ticker = prompt("Ticker symbol").upper()

    if not ticker:
        pause()
        return

    print(f"  Periods: {', '.join(VALID_PERIODS)}")
    period = prompt("Period (default: 1mo)") or "1mo"

    if period not in VALID_PERIODS:
        print(f"  ❌ Invalid period. Choose from: {', '.join(VALID_PERIODS)}")
        pause()
        return

    print(f"  Fetching {period} data for {ticker}…")
    df = tracker.get_historical_data(ticker, period=period)

    if df is None:
        print(f"  ❌ No data returned for '{ticker}'. Check the symbol.")
        pause()
        return

    print("  Generating chart…")
    path = plotter.plot_historical(ticker, df, period)
    print(f"  ✅ Chart saved to: {path}")
    pause()


def plot_comparison():
    hr()
    print("  🔀  Compare Multiple Tickers\n")
    raw = prompt("Enter tickers separated by commas (e.g. AAPL,MSFT,GOOGL)")
    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]

    if len(tickers) < 2:
        print("  ❌ Please enter at least 2 ticker symbols.")
        pause()
        return

    print(f"  Periods: {', '.join(VALID_PERIODS)}")
    period = prompt("Period (default: 1mo)") or "1mo"

    if period not in VALID_PERIODS:
        print(f"  ❌ Invalid period.")
        pause()
        return

    dfs = {}
    for ticker in tickers:
        print(f"  Fetching {ticker}…")
        df = tracker.get_historical_data(ticker, period=period)
        if df is not None:
            dfs[ticker] = df
        else:
            print(f"  ⚠️  No data for {ticker}, skipping.")

    if len(dfs) < 2:
        print("  ❌ Not enough valid tickers to compare.")
        pause()
        return

    path = plotter.plot_comparison(list(dfs.keys()), dfs, period)
    print(f"  ✅ Comparison chart saved to: {path}")
    pause()


def manage_alerts():
    hr()
    print("  🔔  Manage Price Alerts\n")
    print("  [1] View current alerts")
    print("  [2] Add alert")
    print("  [3] Delete alert")
    print("  [4] Back")
    choice = prompt("Choose")

    rules = config.load_alerts()

    if choice == "1":
        if not rules:
            print("\n  (No alerts set.)")
        else:
            print()
            for i, r in enumerate(rules, 1):
                print(f"  [{i}] {r['ticker']}  {r['condition']}  ${r['threshold']:.2f}")

    elif choice == "2":
        ticker = prompt("Ticker symbol").upper()
        condition = prompt("Condition — 'above' or 'below'").lower()
        if condition not in ("above", "below"):
            print("  ❌ Condition must be 'above' or 'below'.")
            pause()
            return
        try:
            threshold = float(prompt("Price threshold (e.g. 150.00)"))
        except ValueError:
            print("  ❌ Invalid price.")
            pause()
            return

        rules.append({"ticker": ticker, "condition": condition, "threshold": threshold})
        config.save_alerts(rules)
        print(f"  ✅ Alert saved: {ticker} {condition} ${threshold:.2f}")

    elif choice == "3":
        if not rules:
            print("\n  (No alerts to delete.)")
        else:
            for i, r in enumerate(rules, 1):
                print(f"  [{i}] {r['ticker']}  {r['condition']}  ${r['threshold']:.2f}")
            try:
                idx = int(prompt("Delete alert number")) - 1
                if 0 <= idx < len(rules):
                    removed = rules.pop(idx)
                    config.save_alerts(rules)
                    print(f"  ✅ Removed: {removed['ticker']} {removed['condition']} ${removed['threshold']:.2f}")
                else:
                    print("  ❌ Invalid number.")
            except ValueError:
                print("  ❌ Invalid input.")

    pause()


def _monitor_job():
    """Background job: check prices and fire any triggered alerts."""
    watchlist = config.load_watchlist()
    rules = config.load_alerts()

    if not watchlist or not rules:
        return

    prices = tracker.get_batch_prices(watchlist)
    triggered = alert_engine.check_alerts(rules, prices)
    if triggered:
        alert_engine.print_alerts(triggered)


def start_monitor():
    hr()
    print("  ⏱️   Starting Price Monitor\n")
    print(f"  Checking every {CHECK_INTERVAL_MINUTES} minute(s). Press Ctrl+C to stop.\n")

    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(_monitor_job)

    # Run once immediately
    _monitor_job()

    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    except KeyboardInterrupt:
        schedule.clear()
        print("\n\n  ✅ Monitor stopped.\n")


def ticker_info():
    hr()
    print("  🔎  Ticker Info\n")
    ticker = prompt("Ticker symbol").upper()
    print(f"  Fetching info for {ticker}…")
    info = tracker.get_ticker_info(ticker)
    price = tracker.get_current_price(ticker)

    if not info and price is None:
        print(f"  ❌ No data found for '{ticker}'.")
        pause()
        return

    print()
    print(f"  Name       : {info.get('name', ticker)}")
    print(f"  Sector     : {info.get('sector', 'N/A')}")
    print(f"  Currency   : {info.get('currency', 'USD')}")
    print(f"  Price      : {fmt_price(price)}")
    print(f"  Market Cap : {fmt_mcap(info.get('market_cap'))}")
    print(f"  52W High   : {fmt_price(info.get('52w_high'))}")
    print(f"  52W Low    : {fmt_price(info.get('52w_low'))}")
    print(f"  P/E Ratio  : {info.get('pe_ratio', 'N/A')}")
    pause()


# ─── Main Loop ────────────────────────────────────────────────────────────────

def main():
    while True:
        clear()
        banner()
        print()
        print("  [1] View watchlist prices")
        print("  [2] Add ticker to watchlist")
        print("  [3] Remove ticker from watchlist")
        print("  [4] Plot historical chart")
        print("  [5] Compare tickers chart")
        print("  [6] Manage price alerts")
        print("  [7] Start price monitor (scheduler)")
        print("  [8] Ticker info & fundamentals")
        print("  [9] Exit")
        print()
        hr()

        choice = prompt("Choose an option")

        if choice == "1":
            view_watchlist()
        elif choice == "2":
            add_ticker()
        elif choice == "3":
            remove_ticker()
        elif choice == "4":
            plot_historical()
        elif choice == "5":
            plot_comparison()
        elif choice == "6":
            manage_alerts()
        elif choice == "7":
            start_monitor()
        elif choice == "8":
            ticker_info()
        elif choice == "9":
            print("\n  👋  Goodbye!\n")
            sys.exit(0)
        else:
            print("  ❌ Invalid option. Please choose 1–9.")
            pause()


if __name__ == "__main__":
    main()
