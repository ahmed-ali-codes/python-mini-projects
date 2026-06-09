# 🔐 Personal Password Manager

A secure, encrypted, command-line password manager built with Python and the `cryptography` library.

## Security Model

| Component | Detail |
|---|---|
| Key Derivation | PBKDF2-HMAC-SHA256 (480,000 iterations) |
| Encryption | Fernet (AES-128-CBC + HMAC-SHA256) |
| Master Password | **Never stored** — only used to derive the key |
| Salt | Randomly generated once, stored in `salt.key` |
| Vault | SQLite database (`vault.db`) — all passwords stored as encrypted ciphertext |

> ⚠️ **Important:** If you lose your master password, your data **cannot be recovered**. There is no reset mechanism by design.

## Features

- 🔑 **Master password authentication** — verified on every launch
- 🗄️ **Encrypted vault** — all data encrypted before being written to disk
- ➕ **Add / Update entries** — store site, username, and password
- 📋 **View all entries** — list every saved entry (decrypted in memory)
- 🔍 **Retrieve a single entry** — look up by site name
- 🎲 **Password generator** — cryptographically secure random passwords via Python's `secrets` module
- 🗑️ **Delete entries** — remove any saved entry

## Setup

```bash
# 1. Clone or navigate to the project
cd password-manager

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

## First Launch

On first run, you will be prompted to **set a master password**. This generates:
- A random `salt.key` file used for key derivation
- A `vault.db` SQLite database containing your encrypted entries

## Usage

After authenticating, you'll see an interactive menu:

```
[1] Add / Update password
[2] View all entries
[3] Retrieve a password
[4] Generate a strong password
[5] Delete an entry
[6] Exit
```

## File Structure

```
password-manager/
├── main.py          # CLI entry point
├── crypto.py        # PBKDF2 key derivation & Fernet encrypt/decrypt
├── database.py      # SQLite CRUD operations
├── password_gen.py  # Secure password generator (secrets module)
├── schema.sql       # Database schema
├── requirements.txt # Python dependencies
├── .gitignore       # Excludes vault.db, salt.key, venv/
└── README.md        # This file
```

> `vault.db` and `salt.key` are excluded from version control via `.gitignore`.

## Dependencies

- [`cryptography`](https://pypi.org/project/cryptography/) — encryption primitives (Fernet, PBKDF2)
