"""
file_renamer.py — Bulk file renaming using pathlib.

Supported operations:
  - Add prefix / suffix to filenames
  - Replace text in filenames
  - Sequential numbering  (file_001.txt, file_002.txt, …)
  - Change file extension
  - Convert filename case (lower / upper / title)
"""

from pathlib import Path


def _get_files(folder: str, extension: str = "") -> list[Path]:
    """Return sorted list of files in folder, optionally filtered by extension."""
    p = Path(folder)
    if not p.is_dir():
        raise NotADirectoryError(f"'{folder}' is not a valid directory.")
    pattern = f"*{extension}" if extension else "*"
    return sorted(f for f in p.glob(pattern) if f.is_file())


def add_prefix(folder: str, prefix: str, extension: str = "") -> list[str]:
    """Add a prefix to every filename."""
    files = _get_files(folder, extension)
    renamed = []
    for f in files:
        new_name = f.parent / f"{prefix}{f.name}"
        f.rename(new_name)
        renamed.append(new_name.name)
    return renamed


def add_suffix(folder: str, suffix: str, extension: str = "") -> list[str]:
    """Add a suffix before the file extension."""
    files = _get_files(folder, extension)
    renamed = []
    for f in files:
        new_name = f.parent / f"{f.stem}{suffix}{f.suffix}"
        f.rename(new_name)
        renamed.append(new_name.name)
    return renamed


def replace_text(folder: str, old: str, new: str, extension: str = "") -> list[str]:
    """Replace a substring in all filenames."""
    files = _get_files(folder, extension)
    renamed = []
    for f in files:
        if old in f.name:
            new_name = f.parent / f.name.replace(old, new)
            f.rename(new_name)
            renamed.append(new_name.name)
    return renamed


def sequential_rename(
    folder: str, base_name: str, start: int = 1,
    padding: int = 3, extension: str = ""
) -> list[str]:
    """Rename files to base_name_001.ext, base_name_002.ext, …"""
    files = _get_files(folder, extension)
    renamed = []
    for i, f in enumerate(files, start=start):
        num = str(i).zfill(padding)
        new_name = f.parent / f"{base_name}_{num}{f.suffix}"
        f.rename(new_name)
        renamed.append(new_name.name)
    return renamed


def change_extension(folder: str, old_ext: str, new_ext: str) -> list[str]:
    """Change all files from old_ext to new_ext (include the dot, e.g. '.txt')."""
    files = _get_files(folder, old_ext)
    renamed = []
    for f in files:
        new_name = f.with_suffix(new_ext)
        f.rename(new_name)
        renamed.append(new_name.name)
    return renamed


def convert_case(folder: str, mode: str = "lower", extension: str = "") -> list[str]:
    """Convert filenames to lower / upper / title case."""
    files = _get_files(folder, extension)
    renamed = []
    for f in files:
        if mode == "lower":
            new_stem = f.stem.lower()
        elif mode == "upper":
            new_stem = f.stem.upper()
        elif mode == "title":
            new_stem = f.stem.title()
        else:
            raise ValueError("mode must be 'lower', 'upper', or 'title'")
        new_name = f.parent / f"{new_stem}{f.suffix}"
        if new_name != f:
            f.rename(new_name)
        renamed.append(new_name.name)
    return renamed
