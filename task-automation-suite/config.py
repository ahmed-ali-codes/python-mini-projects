"""
config.py — Load and save email SMTP configuration to email_config.json.
Credentials are stored locally and are git-ignored.
"""

import json
import os

CONFIG_FILE = "email_config.json"

DEFAULT_CONFIG = {
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "",
    "sender_password": "",
    "default_recipient": "",
}


def load_email_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE) as f:
        return {**DEFAULT_CONFIG, **json.load(f)}


def save_email_config(cfg: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
