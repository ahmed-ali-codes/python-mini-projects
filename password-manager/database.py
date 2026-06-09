"""
database.py — SQLite CRUD operations for the encrypted password vault.

All password values passed to add_entry() must already be encrypted
ciphertext. Decryption is handled in main.py after retrieval.
"""

import sqlite3
import os

DB_FILE = "vault.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the vault database from schema.sql."""
    conn = get_connection()
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def add_entry(site: str, username: str, encrypted_password: str):
    """Insert a new password entry."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO entries (site, username, password) VALUES (?, ?, ?)",
        (site.lower(), username, encrypted_password),
    )
    conn.commit()
    conn.close()


def update_entry(site: str, username: str, encrypted_password: str):
    """Update an existing entry's username and password."""
    conn = get_connection()
    conn.execute(
        "UPDATE entries SET username = ?, password = ? WHERE site = ?",
        (username, encrypted_password, site.lower()),
    )
    conn.commit()
    conn.close()


def get_entry(site: str) -> sqlite3.Row | None:
    """Retrieve a single entry by site name (case-insensitive)."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM entries WHERE site = ?", (site.lower(),)
    ).fetchone()
    conn.close()
    return row


def get_all_entries() -> list[sqlite3.Row]:
    """Retrieve all stored entries."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM entries ORDER BY site").fetchall()
    conn.close()
    return rows


def delete_entry(site: str) -> bool:
    """Delete an entry by site name. Returns True if a row was deleted."""
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM entries WHERE site = ?", (site.lower(),)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def entry_exists(site: str) -> bool:
    """Check if an entry for the given site already exists."""
    return get_entry(site) is not None
