"""
main.py — Multi-Threaded File Downloader CLI

Run with:  python main.py
"""

import sys
import os
import time
from download_manager import DownloadManager

manager = DownloadManager(max_workers=4)

STATUS_ICONS = {
    "pending":     "⏳",
    "downloading": "⬇️ ",
    "paused":      "⏸️ ",
    "done":        "✅",
    "error":       "❌",
    "cancelled":   "🛑",
}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 60)
    print("    ⬇️   Multi-Threaded File Downloader   ⬇️            ")
    print("=" * 60)


def hr():
    print("-" * 60)


def prompt(text: str) -> str:
    return input(f"  {text}: ").strip()


def pause():
    input("\n  Press Enter to continue…")


def progress_bar(pct: float, width: int = 20) -> str:
    filled = int(width * pct / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:5.1f}%"


# ─── Menu Actions ─────────────────────────────────────────────────────────────

def add_download():
    hr()
    print("  ➕  Add Download\n")
    url = prompt("URL to download")
    if not url:
        return
    filename = prompt("Save as (leave blank to auto-detect from URL)")
    task = manager.add(url, filename)
    print(f"\n  ✅ Queued: {task.filename}")
    pause()


def add_multiple():
    hr()
    print("  📋  Add Multiple Downloads\n")
    print("  Enter URLs one per line. Type 'done' when finished.\n")
    count = 0
    while True:
        url = prompt(f"URL {count + 1} ('done' to finish)")
        if url.lower() == "done" or not url:
            break
        filename = prompt("  Save as (blank = auto)")
        task = manager.add(url, filename)
        print(f"  ✅ Queued: {task.filename}")
        count += 1
    if count:
        print(f"\n  ✅ {count} download(s) queued and running in parallel.")
    pause()


def view_status():
    clear()
    banner()
    print("\n  📊  Download Status\n")
    tasks = manager.list_tasks()

    if not tasks:
        print("  (No downloads yet.)")
        pause()
        return

    print(f"  {'#':<4} {'File':<30} {'Status':<14} {'Progress':<28} {'Size'}")
    hr()
    for i, task in enumerate(tasks, 1):
        icon = STATUS_ICONS.get(task.status, "?")
        bar  = progress_bar(task.progress_pct()) if task.status in ("downloading", "paused", "done") else ""
        print(f"  {i:<4} {task.filename[:29]:<30} {icon} {task.status:<12} {bar:<28} {task.size_str()}")
        if task.status == "error":
            print(f"       ⚠️  {task.error}")

    print()
    pause()


def live_monitor():
    """Refresh status every second until all done or user presses Ctrl+C."""
    print("\n  📡  Live Monitor — press Ctrl+C to stop\n")
    try:
        while True:
            clear()
            banner()
            tasks = manager.list_tasks()
            active = [t for t in tasks if t.status in ("downloading", "paused")]

            print(f"\n  Active: {len(active)}  /  Total: {len(tasks)}\n")
            print(f"  {'#':<4} {'File':<30} {'Status':<14} {'Progress':<28} {'Size'}")
            hr()
            for i, task in enumerate(tasks, 1):
                icon = STATUS_ICONS.get(task.status, "?")
                bar  = progress_bar(task.progress_pct()) if task.status in ("downloading", "paused", "done") else ""
                print(f"  {i:<4} {task.filename[:29]:<30} {icon} {task.status:<12} {bar:<28} {task.size_str()}")

            if not active:
                print("\n  ✅ All downloads finished.")
                time.sleep(1)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n  Monitor stopped.")
        time.sleep(0.5)


def control_download(action: str):
    hr()
    tasks = manager.list_tasks()
    if not tasks:
        print("  (No downloads.)")
        pause()
        return

    for i, t in enumerate(tasks, 1):
        icon = STATUS_ICONS.get(t.status, "?")
        print(f"  [{i}] {icon}  {t.filename}  ({t.status})")

    choice = prompt(f"Which download to {action}? (number)")
    try:
        idx = int(choice) - 1
        task = tasks[idx]
        if action == "pause":
            manager.pause(task.filename)
        elif action == "resume":
            manager.resume(task.filename)
        elif action == "cancel":
            manager.cancel(task.filename)
    except (ValueError, IndexError):
        print("  ❌ Invalid selection.")

    pause()


# ─── Main Loop ────────────────────────────────────────────────────────────────

def main():
    while True:
        clear()
        banner()
        print()
        print("  [1] Add a download")
        print("  [2] Add multiple downloads (parallel)")
        print("  [3] View download status")
        print("  [4] Live monitor (auto-refresh)")
        print("  [5] Pause a download")
        print("  [6] Resume a download")
        print("  [7] Cancel a download")
        print("  [8] Wait for all to finish")
        print("  [9] Exit")
        print()
        hr()

        choice = prompt("Choose an option")

        if choice == "1":
            add_download()
        elif choice == "2":
            add_multiple()
        elif choice == "3":
            view_status()
        elif choice == "4":
            live_monitor()
        elif choice == "5":
            control_download("pause")
        elif choice == "6":
            control_download("resume")
        elif choice == "7":
            control_download("cancel")
        elif choice == "8":
            print("\n  ⏳  Waiting for all downloads to complete…")
            manager.wait_all()
            print("  ✅  All done!")
            pause()
        elif choice == "9":
            print("\n  👋  Shutting down…")
            manager.shutdown(wait=False)
            sys.exit(0)
        else:
            print("  ❌ Invalid option.")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
