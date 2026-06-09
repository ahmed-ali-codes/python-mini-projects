"""
plotter.py — Matplotlib chart generation for historical stock data.

Charts are saved as PNG files to the charts/ directory.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

CHARTS_DIR = "charts"


def _ensure_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)


def _get_close(df: pd.DataFrame) -> pd.Series:
    """Extract the Close column, handling MultiIndex columns from yfinance."""
    if isinstance(df.columns, pd.MultiIndex):
        return df["Close"].iloc[:, 0]
    return df["Close"]


def _get_volume(df: pd.DataFrame) -> pd.Series:
    """Extract the Volume column, handling MultiIndex columns from yfinance."""
    if isinstance(df.columns, pd.MultiIndex):
        return df["Volume"].iloc[:, 0]
    return df["Volume"]


def plot_historical(ticker: str, df: pd.DataFrame, period: str = "") -> str:
    """
    Plot a styled candlestick-style closing price chart with volume bars
    and 7-day / 20-day moving averages.

    Returns the path to the saved PNG file.
    """
    _ensure_charts_dir()

    close = _get_close(df)
    volume = _get_volume(df)

    ma7 = close.rolling(window=7).mean()
    ma20 = close.rolling(window=20).mean()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(13, 8),
        gridspec_kw={"height_ratios": [3, 1]},
        facecolor="#0d1117",
    )
    fig.suptitle(
        f"{ticker}  —  Historical Price  ({period})",
        color="white", fontsize=15, fontweight="bold", y=0.97,
    )

    # ── Price chart ──────────────────────────────────────────────────────────
    ax1.set_facecolor("#0d1117")
    ax1.plot(close.index, close, color="#58a6ff", linewidth=1.8, label="Close")
    ax1.fill_between(close.index, close, close.min(), alpha=0.15, color="#58a6ff")

    if len(close) >= 7:
        ax1.plot(ma7.index, ma7, color="#f0883e", linewidth=1.2,
                 linestyle="--", label="MA 7")
    if len(close) >= 20:
        ax1.plot(ma20.index, ma20, color="#3fb950", linewidth=1.2,
                 linestyle="--", label="MA 20")

    ax1.set_ylabel("Price (USD)", color="#8b949e")
    ax1.tick_params(colors="#8b949e", labelsize=9)
    ax1.spines[:].set_color("#30363d")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right")
    ax1.legend(facecolor="#161b22", labelcolor="white", fontsize=9)
    ax1.grid(color="#21262d", linewidth=0.6)

    # ── Volume bars ───────────────────────────────────────────────────────────
    ax2.set_facecolor("#0d1117")
    bar_colors = ["#3fb950" if c >= o else "#f85149"
                  for c, o in zip(close, df["Open"].iloc[:, 0]
                                  if isinstance(df.columns, pd.MultiIndex)
                                  else df["Open"])]
    ax2.bar(volume.index, volume, color=bar_colors, alpha=0.7, width=0.8)
    ax2.set_ylabel("Volume", color="#8b949e")
    ax2.tick_params(colors="#8b949e", labelsize=8)
    ax2.spines[:].set_color("#30363d")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha="right")
    ax2.grid(color="#21262d", linewidth=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    date_str = datetime.now().strftime("%Y%m%d")
    filename = os.path.join(CHARTS_DIR, f"{ticker}_{period}_{date_str}.png")
    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor="#0d1117")
    plt.close()
    return filename


def plot_comparison(tickers: list[str], dfs: dict[str, pd.DataFrame], period: str = "") -> str:
    """
    Plot normalised closing prices for multiple tickers on one chart,
    so percentage gains/losses are directly comparable.

    Returns the path to the saved PNG file.
    """
    _ensure_charts_dir()

    colors = ["#58a6ff", "#f0883e", "#3fb950", "#bc8cff", "#f85149",
              "#e3b341", "#39d353", "#ff7b72"]

    fig, ax = plt.subplots(figsize=(13, 6), facecolor="#0d1117")
    fig.suptitle(
        f"Normalised Comparison  ({period})",
        color="white", fontsize=14, fontweight="bold",
    )
    ax.set_facecolor("#0d1117")

    for i, (ticker, df) in enumerate(dfs.items()):
        close = _get_close(df)
        normalised = (close / close.iloc[0]) * 100  # base = 100
        ax.plot(
            normalised.index, normalised,
            color=colors[i % len(colors)],
            linewidth=1.8,
            label=ticker,
        )

    ax.axhline(100, color="#30363d", linewidth=0.8, linestyle="--")
    ax.set_ylabel("Normalised Price (base = 100)", color="#8b949e")
    ax.tick_params(colors="#8b949e", labelsize=9)
    ax.spines[:].set_color("#30363d")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
    ax.legend(facecolor="#161b22", labelcolor="white", fontsize=10)
    ax.grid(color="#21262d", linewidth=0.6)

    plt.tight_layout()

    date_str = datetime.now().strftime("%Y%m%d")
    label = "_".join(dfs.keys())
    filename = os.path.join(CHARTS_DIR, f"compare_{label}_{date_str}.png")
    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor="#0d1117")
    plt.close()
    return filename
