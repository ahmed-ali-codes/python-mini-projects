"""
tracker.py — Fetch live and historical stock data via yfinance.
"""

import yfinance as yf
import pandas as pd


def get_current_price(ticker: str) -> float | None:
    """
    Return the latest market price for a ticker.
    Returns None if the ticker is invalid or data is unavailable.
    """
    try:
        data = yf.Ticker(ticker)
        info = data.fast_info
        price = info.last_price
        return round(float(price), 2) if price else None
    except Exception:
        return None


def get_batch_prices(tickers: list[str]) -> dict[str, float | None]:
    """
    Fetch current prices for multiple tickers at once.
    Returns a dict mapping ticker → price (or None on failure).
    """
    results = {}
    for ticker in tickers:
        results[ticker] = get_current_price(ticker)
    return results


def get_historical_data(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
) -> pd.DataFrame | None:
    """
    Fetch OHLCV historical data as a DataFrame.

    Args:
        ticker:   Stock symbol (e.g. "AAPL")
        period:   One of: 1d, 5d, 1wk, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: One of: 1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo

    Returns:
        DataFrame with columns [Open, High, Low, Close, Volume] or None.
    """
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if df.empty:
            return None
        return df
    except Exception:
        return None


def get_ticker_info(ticker: str) -> dict:
    """
    Return a summary dict with name, sector, market cap, etc.
    Falls back to empty dict if data is unavailable.
    """
    try:
        info = yf.Ticker(ticker).info
        return {
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "pe_ratio": info.get("trailingPE"),
        }
    except Exception:
        return {}
