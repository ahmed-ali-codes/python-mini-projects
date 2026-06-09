"""
config.py — Persist watchlist tickers and alert rules to JSON files.
"""

import json
import os

WATCHLIST_FILE = "watchlist.json"
ALERTS_FILE = "alerts.json"


def load_watchlist() -> list[str]:
    """Load the list of watched ticker symbols."""
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE) as f:
        return json.load(f)


def save_watchlist(tickers: list[str]):
    """Save the watchlist to disk."""
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(sorted(set(t.upper() for t in tickers)), f, indent=2)


def load_alerts() -> list[dict]:
    """Load saved alert rules."""
    if not os.path.exists(ALERTS_FILE):
        return []
    with open(ALERTS_FILE) as f:
        return json.load(f)


def save_alerts(rules: list[dict]):
    """Save alert rules to disk."""
    with open(ALERTS_FILE, "w") as f:
        json.dump(rules, f, indent=2)
