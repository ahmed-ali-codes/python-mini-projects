"""
downloader.py — Core single-file download logic.

Key features:
  - HTTP Range requests for resumable downloads
  - threading.Event for pause / resume control
  - tqdm progress bar per download
  - Session state saved after every chunk
"""

import threading
import requests
from pathlib import Path
from tqdm import tqdm
import session as session_store

DOWNLOAD_DIR = Path("downloads")
CHUNK_SIZE   = 1024 * 64   # 64 KB


def _ensure_download_dir():
    DOWNLOAD_DIR.mkdir(exist_ok=True)


class DownloadTask:
    """Represents a single file download with pause/resume support."""

    def __init__(self, url: str, filename: str = ""):
        self.url          = url
        self.filename     = filename or Path(url.split("?")[0]).name or "download"
        self.dest         = str(DOWNLOAD_DIR / self.filename)

        self._pause_event = threading.Event()
        self._pause_event.set()          # not paused initially
        self._stop_event  = threading.Event()

        self.status       = "pending"    # pending | downloading | paused | done | error
        self.bytes_done   = 0
        self.total_size   = 0
        self.error        = ""

    # ── Control ──────────────────────────────────────────────────────────────

    def pause(self):
        self._pause_event.clear()
        self.status = "paused"

    def resume(self):
        self._pause_event.set()
        self.status = "downloading"

    def cancel(self):
        self._stop_event.set()
        self._pause_event.set()   # unblock if paused
        self.status = "cancelled"

    @property
    def is_paused(self) -> bool:
        return not self._pause_event.is_set()

    # ── Download ─────────────────────────────────────────────────────────────

    def start(self):
        """Begin or resume downloading. Blocks until done (run in a thread)."""
        _ensure_download_dir()

        # Check for an existing session (resume)
        saved = session_store.load_session(self.dest)
        if saved and Path(self.dest).exists():
            self.bytes_done = saved["bytes_downloaded"]
            self.total_size = saved["total_size"]
        else:
            self.bytes_done = 0

        headers = {}
        if self.bytes_done > 0:
            headers["Range"] = f"bytes={self.bytes_done}-"

        try:
            self.status = "downloading"
            response = requests.get(self.url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()

            # Content-Range tells us the real total; fall back to Content-Length
            content_length = int(response.headers.get("Content-Length", 0))
            if self.total_size == 0:
                self.total_size = self.bytes_done + content_length

            write_mode = "ab" if self.bytes_done > 0 else "wb"

            with open(self.dest, write_mode) as f, tqdm(
                total=self.total_size,
                initial=self.bytes_done,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"  {self.filename[:30]:<30}",
                leave=False,
                dynamic_ncols=True,
            ) as bar:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    # Honour stop signal
                    if self._stop_event.is_set():
                        return

                    # Honour pause signal — block here until resumed
                    self._pause_event.wait()

                    if self._stop_event.is_set():
                        return

                    f.write(chunk)
                    self.bytes_done += len(chunk)
                    bar.update(len(chunk))

                    # Persist session every chunk for reliable resume
                    session_store.save_session(
                        self.dest, self.url, self.bytes_done, self.total_size
                    )

            # Finished
            session_store.clear_session(self.dest)
            self.status = "done"

        except Exception as exc:
            self.error  = str(exc)
            self.status = "error"

    def size_str(self) -> str:
        def fmt(b):
            if b >= 1_073_741_824: return f"{b/1_073_741_824:.1f} GB"
            if b >= 1_048_576:     return f"{b/1_048_576:.1f} MB"
            if b >= 1024:          return f"{b/1024:.1f} KB"
            return f"{b} B"
        if self.total_size:
            return f"{fmt(self.bytes_done)} / {fmt(self.total_size)}"
        return fmt(self.bytes_done)

    def progress_pct(self) -> float:
        if not self.total_size:
            return 0.0
        return round(self.bytes_done / self.total_size * 100, 1)
