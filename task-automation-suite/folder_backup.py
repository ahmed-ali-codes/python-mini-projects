"""
folder_backup.py — Automated folder backup using shutil and pathlib.

Creates timestamped ZIP archives of source folders in a backups/ directory.
Supports keeping only the N most recent backups to save disk space.
"""

import shutil
import os
from pathlib import Path
from datetime import datetime


BACKUP_DIR = Path("backups")


def _ensure_backup_dir():
    BACKUP_DIR.mkdir(exist_ok=True)


def create_backup(source_folder: str, label: str = "") -> str:
    """
    Create a ZIP archive of source_folder.

    Args:
        source_folder: Path to the folder to back up.
        label:         Optional name prefix (defaults to folder name).

    Returns:
        Path to the created ZIP file.
    """
    _ensure_backup_dir()
    source = Path(source_folder)

    if not source.is_dir():
        raise NotADirectoryError(f"'{source_folder}' is not a valid directory.")

    name = label or source.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = BACKUP_DIR / f"{name}_{timestamp}"

    # shutil.make_archive appends .zip automatically
    result = shutil.make_archive(str(archive_name), "zip", root_dir=str(source.parent), base_dir=source.name)
    return result


def list_backups() -> list[Path]:
    """Return sorted list of all backup ZIP files (newest first)."""
    if not BACKUP_DIR.exists():
        return []
    return sorted(BACKUP_DIR.glob("*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)


def prune_backups(keep: int = 5):
    """
    Delete oldest backup archives, keeping only the `keep` most recent.

    Args:
        keep: Number of backups to retain.
    """
    backups = list_backups()
    to_delete = backups[keep:]
    for b in to_delete:
        b.unlink()
    return to_delete


def get_backup_info(path: Path) -> dict:
    """Return metadata dict for a backup archive."""
    stat = path.stat()
    return {
        "name": path.name,
        "size_mb": round(stat.st_size / 1_048_576, 2),
        "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }
