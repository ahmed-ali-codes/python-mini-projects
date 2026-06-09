"""
session.py — Persist and restore download progress for pause/resume.

State is saved as a JSON file alongside the partial download:
  <filename>.session  →  { url, dest, bytes_downloaded, total_size }
"""

import json
import os
from pathlib import Path


def session_path(dest: str) -> str:
    return dest + ".session"


def save_session(dest: str, url: str, bytes_downloaded: int, total_size: int):
    data = {
        "url": url,
        "dest": dest,
        "bytes_downloaded": bytes_downloaded,
        "total_size": total_size,
    }
    with open(session_path(dest), "w") as f:
        json.dump(data, f)


def load_session(dest: str) -> dict | None:
    path = session_path(dest)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def clear_session(dest: str):
    path = session_path(dest)
    if os.path.exists(path):
        os.remove(path)
