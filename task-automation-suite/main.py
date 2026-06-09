"""
main.py — Task Automation Suite CLI

Run with:  python main.py
"""

import sys
import os

import config
import file_renamer
import folder_backup
import pdf_reporter
import email_notifier


# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 58)
    print("       ⚙️   Task Automation Suite   ⚙️              ")
    print("=" * 58)


def hr():
    print("-" * 58)


def prompt(text: str) -> str:
    return input(f"  {text}: ").strip()


def pause():
    input("\n  Press Enter to continue…")


# ─── 1. File Renamer ─────────────────────────────────────────────────────────

def menu_file_renamer():
    while True:
        clear()
        banner()
        print("\n  📁  Bulk File Renamer\n")
        print("  [1] Add prefix to filenames")
        print("  [2] Add suffix to filenames")
        print("  [3] Replace text in filenames")
        print("  [4] Sequential numbering")
        print("  [5] Change file extension")
        print("  [6] Convert filename case")
        print("  [7] Back")
        hr()
        choice = prompt("Choose")

        if choice == "7":
            break

        folder = prompt("Folder path")
        if not os.path.isdir(folder):
            print(f"\n  ❌ '{folder}' is not a valid directory.")
            pause()
            continue

        ext = prompt("Filter by extension (leave blank for all, e.g. .txt)") or ""

        try:
            if choice == "1":
                prefix = prompt("Prefix to add")
                renamed = file_renamer.add_prefix(folder, prefix, ext)
            elif choice == "2":
                suffix = prompt("Suffix to add")
                renamed = file_renamer.add_suffix(folder, suffix, ext)
            elif choice == "3":
                old = prompt("Text to find")
                new = prompt("Replace with")
                renamed = file_renamer.replace_text(folder, old, new, ext)
            elif choice == "4":
                base = prompt("Base name (e.g. 'photo')")
                start = int(prompt("Start number (default 1)") or "1")
                renamed = file_renamer.sequential_rename(folder, base, start, extension=ext)
            elif choice == "5":
                old_ext = prompt("Current extension (e.g. .txt)")
                new_ext = prompt("New extension (e.g. .md)")
                renamed = file_renamer.change_extension(folder, old_ext, new_ext)
            elif choice == "6":
                mode = prompt("Case mode — lower / upper / title (default lower)") or "lower"
                renamed = file_renamer.convert_case(folder, mode, ext)
            else:
                print("  ❌ Invalid option.")
                pause()
                continue

            print(f"\n  ✅ Renamed {len(renamed)} file(s):")
            for name in renamed[:10]:
                print(f"     → {name}")
            if len(renamed) > 10:
                print(f"     … and {len(renamed) - 10} more")

        except Exception as e:
            print(f"\n  ❌ Error: {e}")

        pause()


# ─── 2. PDF Report Generator ──────────────────────────────────────────────────

def menu_pdf_report():
    clear()
    banner()
    print("\n  📄  PDF Report Generator\n")

    title = prompt("Report title") or "Automation Report"
    sections = []

    print("\n  Add sections (type 'done' as heading to finish):\n")
    while True:
        heading = prompt("Section heading ('done' to finish)")
        if heading.lower() == "done" or not heading:
            break

        section: dict = {"heading": heading}

        text = prompt("Body text (leave blank to skip)")
        if text:
            section["text"] = text

        add_kv = prompt("Add key-value table? (y/n)").lower() == "y"
        if add_kv:
            kv_rows = []
            print("  Enter key-value pairs ('done' to stop):")
            while True:
                key = prompt("  Key ('done' to stop)")
                if key.lower() == "done" or not key:
                    break
                val = prompt("  Value")
                kv_rows.append((key, val))
            if kv_rows:
                section["kv"] = kv_rows

        sections.append(section)

    if not sections:
        sections = [{
            "heading": "Summary",
            "text": "No sections were added. This is a placeholder report.",
        }]

    filename = prompt("Output filename (leave blank for auto)") or ""
    if filename and not filename.endswith(".pdf"):
        filename += ".pdf"

    try:
        path = pdf_reporter.generate_report(title, sections, filename)
        print(f"\n  ✅ PDF saved to: {path}")
    except Exception as e:
        print(f"\n  ❌ Error generating PDF: {e}")

    pause()


# ─── 3. Email Notifier ───────────────────────────────────────────────────────

def menu_email():
    while True:
        clear()
        banner()
        print("\n  📧  Email Notifier\n")
        print("  [1] Configure SMTP settings")
        print("  [2] Send a plain text email")
        print("  [3] Send an HTML email")
        print("  [4] Back")
        hr()
        choice = prompt("Choose")

        if choice == "4":
            break

        cfg = config.load_email_config()

        if choice == "1":
            print(f"\n  Current host : {cfg['smtp_host']} : {cfg['smtp_port']}")
            print(f"  Sender       : {cfg['sender_email'] or '(not set)'}\n")
            cfg["smtp_host"]         = prompt(f"SMTP host [{cfg['smtp_host']}]") or cfg["smtp_host"]
            cfg["smtp_port"]         = int(prompt(f"SMTP port [{cfg['smtp_port']}]") or cfg["smtp_port"])
            cfg["sender_email"]      = prompt("Sender email") or cfg["sender_email"]
            import getpass
            pw = getpass.getpass("  Sender password (leave blank to keep current): ")
            if pw:
                cfg["sender_password"] = pw
            cfg["default_recipient"] = prompt("Default recipient email") or cfg["default_recipient"]
            config.save_email_config(cfg)
            print("\n  ✅ SMTP settings saved.")
            pause()
            continue

        if not cfg["sender_email"] or not cfg["sender_password"]:
            print("\n  ❌ SMTP not configured. Choose option [1] first.")
            pause()
            continue

        recipient = prompt(f"Recipient [{cfg['default_recipient']}]") or cfg["default_recipient"]
        subject   = prompt("Subject")
        body      = prompt("Message body")

        attach_input = prompt("Attach files? Comma-separated paths (leave blank to skip)")
        attachments = [a.strip() for a in attach_input.split(",") if a.strip()] if attach_input else []

        try:
            if choice == "2":
                email_notifier.send_email(
                    cfg["smtp_host"], cfg["smtp_port"],
                    cfg["sender_email"], cfg["sender_password"],
                    recipient, subject, body,
                    html=False, attachments=attachments,
                )
            elif choice == "3":
                lines = [l.strip() for l in body.split("|") if l.strip()]
                html_body = email_notifier.build_html_body(subject, lines or [body])
                email_notifier.send_email(
                    cfg["smtp_host"], cfg["smtp_port"],
                    cfg["sender_email"], cfg["sender_password"],
                    recipient, subject, html_body,
                    html=True, attachments=attachments,
                )
            print(f"\n  ✅ Email sent to {recipient}!")
        except Exception as e:
            print(f"\n  ❌ Failed to send email: {e}")

        pause()


# ─── 4. Folder Backup ────────────────────────────────────────────────────────

def menu_backup():
    while True:
        clear()
        banner()
        print("\n  🗄️   Folder Backup\n")
        print("  [1] Create backup")
        print("  [2] List backups")
        print("  [3] Prune old backups")
        print("  [4] Back")
        hr()
        choice = prompt("Choose")

        if choice == "4":
            break

        if choice == "1":
            folder = prompt("Folder to back up")
            label  = prompt("Label / name (leave blank to use folder name)") or ""
            try:
                path = folder_backup.create_backup(folder, label)
                info = folder_backup.get_backup_info(__import__("pathlib").Path(path))
                print(f"\n  ✅ Backup created: {info['name']}  ({info['size_mb']} MB)")
            except Exception as e:
                print(f"\n  ❌ Error: {e}")

        elif choice == "2":
            backups = folder_backup.list_backups()
            if not backups:
                print("\n  (No backups found.)")
            else:
                print(f"\n  {'#':<4} {'Name':<45} {'Size (MB)':>10} {'Created'}")
                hr()
                for i, b in enumerate(backups, 1):
                    info = folder_backup.get_backup_info(b)
                    print(f"  {i:<4} {info['name']:<45} {info['size_mb']:>10} {info['created']}")

        elif choice == "3":
            keep = int(prompt("How many recent backups to keep? (default 5)") or "5")
            deleted = folder_backup.prune_backups(keep)
            if deleted:
                print(f"\n  ✅ Deleted {len(deleted)} old backup(s):")
                for d in deleted:
                    print(f"     🗑️  {d.name}")
            else:
                print("\n  ✅ Nothing to prune.")

        pause()


# ─── Main Menu ────────────────────────────────────────────────────────────────

def main():
    while True:
        clear()
        banner()
        print()
        print("  [1] 📁  Bulk File Renamer")
        print("  [2] 📄  PDF Report Generator")
        print("  [3] 📧  Email Notifier")
        print("  [4] 🗄️   Folder Backup")
        print("  [5] 🚪  Exit")
        print()
        hr()

        choice = prompt("Choose a tool")

        if choice == "1":
            menu_file_renamer()
        elif choice == "2":
            menu_pdf_report()
        elif choice == "3":
            menu_email()
        elif choice == "4":
            menu_backup()
        elif choice == "5":
            print("\n  👋  Goodbye!\n")
            sys.exit(0)
        else:
            print("  ❌ Invalid option. Please choose 1–5.")
            pause()


if __name__ == "__main__":
    main()
