"""
alerts.py — Price alert rule engine.

Alert rule format:
    {
        "ticker":     "AAPL",
        "condition":  "above" | "below",
        "threshold":  150.0
    }

Triggered alerts are printed to the console with a bell/timestamp.
"""

from datetime import datetime


def check_alerts(
    rules: list[dict],
    prices: dict[str, float | None],
) -> list[dict]:
    """
    Compare each rule against current prices.

    Returns a list of triggered rules enriched with 'current_price'.
    """
    triggered = []
    for rule in rules:
        ticker = rule["ticker"]
        current = prices.get(ticker)
        if current is None:
            continue

        condition = rule["condition"]
        threshold = rule["threshold"]

        if condition == "above" and current > threshold:
            triggered.append({**rule, "current_price": current})
        elif condition == "below" and current < threshold:
            triggered.append({**rule, "current_price": current})

    return triggered


def format_alert(alert: dict) -> str:
    """Format a triggered alert as a human-readable console string."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arrow = "📈" if alert["condition"] == "above" else "📉"
    return (
        f"\n  🔔  ALERT  [{ts}]\n"
        f"  {arrow}  {alert['ticker']} is {alert['condition']} "
        f"${alert['threshold']:.2f}  →  Current: ${alert['current_price']:.2f}"
    )


def print_alerts(triggered: list[dict]):
    """Print all triggered alerts to stdout."""
    for alert in triggered:
        print(format_alert(alert))
