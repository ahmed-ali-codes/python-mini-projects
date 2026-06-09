"""
main.py — Personal Password Manager CLI

Run with:  python main.py

On first launch:
  - You will be prompted to set a master password.
  - A random salt is generated and saved to salt.key.
  - A vault database (vault.db) is initialised.

On subsequent launches:
  - You must enter the same master password to decrypt your vault.
  - An incorrect master password will be rejected gracefully.
"""

import os
import sys
import getpass
from cryptography.fernet import InvalidToken

import database
import crypto
import password_gen

# ─── Sentinel entry used to verify the master password ──────────────────────
SENTINEL_SITE = "__master_verify__"
SENTINEL_VALUE = "password-manager-v1"


# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 54)
    print("         🔐  Personal Password Manager  🔐          ")
    print("=" * 54)


def hr():
    print("-" * 54)


def prompt(text: str) -> str:
    return input(f"  {text}: ").strip()


def pause():
    input("\n  Press Enter to continue…")


# ─── Authentication ───────────────────────────────────────────────────────────

def first_run_setup() -> crypto.Fernet:
    """Guide the user through setting a master password for the first time."""
    print("\n  👋  Welcome! This looks like your first time.")
    print("  Let's set up your master password.\n")
    print("  ⚠️  IMPORTANT: If you forget your master password,")
    print("     your vault data CANNOT be recovered.\n")

    while True:
        pw = getpass.getpass("  Set master password: ")
        pw2 = getpass.getpass("  Confirm master password: ")
        if pw != pw2:
            print("  ❌ Passwords do not match. Try again.\n")
            continue
        if len(pw) < 8:
            print("  ❌ Password must be at least 8 characters.\n")
            continue
        break

    fernet = crypto.get_fernet(pw)
    # Store an encrypted sentinel so we can verify future logins
    sentinel_enc = crypto.encrypt(SENTINEL_VALUE, fernet)
    database.add_entry(SENTINEL_SITE, "system", sentinel_enc)
    print("\n  ✅ Master password set. Vault created!\n")
    return fernet


def authenticate() -> crypto.Fernet:
    """Prompt for the master password and verify it against the sentinel."""
    print()
    pw = getpass.getpass("  Enter master password: ")
    fernet = crypto.get_fernet(pw)

    sentinel_row = database.get_entry(SENTINEL_SITE)
    if sentinel_row is None:
        print("  ❌ Vault appears corrupt (no sentinel). Exiting.")
        sys.exit(1)

    try:
        decrypted = crypto.decrypt(sentinel_row["password"], fernet)
        if decrypted != SENTINEL_VALUE:
            raise InvalidToken
    except InvalidToken:
        print("\n  ❌ Incorrect master password. Access denied.")
        sys.exit(1)

    print("  ✅ Authenticated!\n")
    return fernet


def get_fernet_instance() -> crypto.Fernet:
    """Initialise DB and either do first-run setup or authenticate."""
    is_new = not os.path.exists(database.DB_FILE)
    database.init_db()

    if is_new or database.get_entry(SENTINEL_SITE) is None:
        return first_run_setup()
    return authenticate()


# ─── Menu Actions ─────────────────────────────────────────────────────────────

def add_password(fernet):
    hr()
    print("  ➕  Add New Password\n")
    site = prompt("Site / Service name (e.g. github.com)")
    if not site:
        print("  ❌ Site name cannot be empty.")
        pause()
        return

    if database.entry_exists(site):
        print(f"  ⚠️  An entry for '{site}' already exists.")
        overwrite = prompt("Overwrite? (y/n)").lower()
        if overwrite != "y":
            pause()
            return

    username = prompt("Username / Email")
    print("  (Leave blank to generate a strong password)")
    password = getpass.getpass("  Password: ")

    if not password:
        password = password_gen.generate_password()
        print(f"  🔑 Generated password: {password}")

    enc_password = crypto.encrypt(password, fernet)

    if database.entry_exists(site):
        database.update_entry(site, username, enc_password)
        print(f"\n  ✅ Entry for '{site}' updated.")
    else:
        database.add_entry(site, username, enc_password)
        print(f"\n  ✅ Entry for '{site}' saved.")

    pause()


def view_all(fernet):
    hr()
    print("  📋  All Saved Entries\n")
    rows = [r for r in database.get_all_entries() if r["site"] != SENTINEL_SITE]

    if not rows:
        print("  (No entries yet.)")
        pause()
        return

    print(f"  {'#':<4} {'Site':<25} {'Username':<25} {'Password'}")
    hr()
    for i, row in enumerate(rows, 1):
        try:
            pw = crypto.decrypt(row["password"], fernet)
        except InvalidToken:
            pw = "<decryption error>"
        print(f"  {i:<4} {row['site']:<25} {row['username']:<25} {pw}")

    pause()


def retrieve_password(fernet):
    hr()
    print("  🔍  Retrieve a Password\n")
    site = prompt("Site / Service name")
    row = database.get_entry(site)

    if row is None or row["site"] == SENTINEL_SITE:
        print(f"  ❌ No entry found for '{site}'.")
        pause()
        return

    try:
        pw = crypto.decrypt(row["password"], fernet)
    except InvalidToken:
        print("  ❌ Decryption failed — vault may be corrupt.")
        pause()
        return

    print(f"\n  Site     : {row['site']}")
    print(f"  Username : {row['username']}")
    print(f"  Password : {pw}")
    print(f"  Saved on : {row['created_at']}")
    pause()


def generate_password_menu():
    hr()
    print("  🔑  Password Generator\n")
    try:
        length = int(prompt("Length (default 16)") or "16")
    except ValueError:
        length = 16

    symbols_input = prompt("Include symbols? (y/n, default y)").lower()
    use_symbols = symbols_input != "n"

    digits_input = prompt("Include digits? (y/n, default y)").lower()
    use_digits = digits_input != "n"

    try:
        password = password_gen.generate_password(
            length=length,
            use_symbols=use_symbols,
            use_digits=use_digits,
        )
    except ValueError as e:
        print(f"  ❌ {e}")
        pause()
        return

    print(f"\n  Generated: {password}")
    pause()


def delete_password():
    hr()
    print("  🗑️  Delete an Entry\n")
    site = prompt("Site / Service name to delete")

    if site.lower() == SENTINEL_SITE:
        print("  ❌ Cannot delete system entry.")
        pause()
        return

    confirm = prompt(f"Are you sure you want to delete '{site}'? (yes/no)").lower()
    if confirm != "yes":
        print("  Cancelled.")
        pause()
        return

    if database.delete_entry(site):
        print(f"  ✅ Entry for '{site}' deleted.")
    else:
        print(f"  ❌ No entry found for '{site}'.")
    pause()


# ─── Main Loop ────────────────────────────────────────────────────────────────

def main():
    clear()
    banner()
    fernet = get_fernet_instance()

    while True:
        clear()
        banner()
        print()
        print("  [1] Add / Update password")
        print("  [2] View all entries")
        print("  [3] Retrieve a password")
        print("  [4] Generate a strong password")
        print("  [5] Delete an entry")
        print("  [6] Exit")
        print()
        hr()

        choice = prompt("Choose an option")

        if choice == "1":
            add_password(fernet)
        elif choice == "2":
            view_all(fernet)
        elif choice == "3":
            retrieve_password(fernet)
        elif choice == "4":
            generate_password_menu()
        elif choice == "5":
            delete_password()
        elif choice == "6":
            print("\n  👋  Goodbye! Stay secure.\n")
            sys.exit(0)
        else:
            print("  ❌ Invalid option. Please choose 1–6.")
            pause()


if __name__ == "__main__":
    main()
