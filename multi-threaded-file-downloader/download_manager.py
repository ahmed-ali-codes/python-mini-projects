"""
download_manager.py — Manage multiple concurrent downloads.

Uses concurrent.futures.ThreadPoolExecutor so downloads run in parallel.
Each DownloadTask is tracked in a registry for pause / resume / cancel.
"""

import threading
from concurrent.futures import ThreadPoolExecutor, Future
from downloader import DownloadTask


class DownloadManager:
    """Orchestrates multiple concurrent DownloadTask instances."""

    def __init__(self, max_workers: int = 4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="dl")
        self._tasks: dict[str, DownloadTask] = {}   # filename → task
        self._futures: dict[str, Future]     = {}
        self._lock = threading.Lock()

    # ── Submit ────────────────────────────────────────────────────────────────

    def add(self, url: str, filename: str = "") -> DownloadTask:
        """Queue a new download and return the DownloadTask."""
        task = DownloadTask(url, filename)
        key  = task.filename

        with self._lock:
            # Prevent duplicate active downloads of the same filename
            if key in self._tasks and self._tasks[key].status in ("downloading", "paused"):
                print(f"  ⚠️  '{key}' is already downloading.")
                return self._tasks[key]
            self._tasks[key] = task

        future = self._executor.submit(task.start)
        with self._lock:
            self._futures[key] = future

        return task

    # ── Control ───────────────────────────────────────────────────────────────

    def pause(self, filename: str):
        task = self._tasks.get(filename)
        if task and task.status == "downloading":
            task.pause()
            print(f"  ⏸️   Paused: {filename}")
        else:
            print(f"  ⚠️  Cannot pause '{filename}' (status: {task.status if task else 'not found'})")

    def resume(self, filename: str):
        task = self._tasks.get(filename)
        if task:
            if task.status == "paused":
                task.resume()
                print(f"  ▶️   Resumed: {filename}")
            elif task.status in ("done", "error", "cancelled"):
                # Re-queue the download from where it left off
                print(f"  🔄  Re-queuing: {filename}")
                new_task = DownloadTask(task.url, filename)
                with self._lock:
                    self._tasks[filename] = new_task
                future = self._executor.submit(new_task.start)
                with self._lock:
                    self._futures[filename] = future
        else:
            print(f"  ❌ No task found for '{filename}'")

    def cancel(self, filename: str):
        task = self._tasks.get(filename)
        if task:
            task.cancel()
            print(f"  🛑  Cancelled: {filename}")
        else:
            print(f"  ❌ No task found for '{filename}'")

    def cancel_all(self):
        for task in self._tasks.values():
            if task.status in ("downloading", "paused"):
                task.cancel()

    # ── Status ────────────────────────────────────────────────────────────────

    def list_tasks(self) -> list[DownloadTask]:
        with self._lock:
            return list(self._tasks.values())

    def wait_all(self):
        """Block until all queued downloads finish."""
        for future in list(self._futures.values()):
            future.result()

    def shutdown(self, wait: bool = True):
        self.cancel_all()
        self._executor.shutdown(wait=wait)
