# ⚙️ Task Automation Suite

A collection of real-world automation tools built with Python — no heavy frameworks, just powerful standard library modules plus `fpdf2`.

## Tools Included

| # | Tool | Description |
|---|---|---|
| 1 | 📁 **File Renamer** | Bulk rename files — prefix, suffix, replace, sequential numbering, extension change, case convert |
| 2 | 📄 **PDF Report Generator** | Generate styled PDF reports with headings, key-value tables and data tables |
| 3 | 📧 **Email Notifier** | Send plain text or HTML emails with attachments via SMTP |
| 4 | 🗄️ **Folder Backup** | Create timestamped ZIP backups, list archives, auto-prune old ones |

## Libraries

| Library | Purpose |
|---|---|
| `pathlib` *(stdlib)* | File & path operations |
| `shutil` *(stdlib)* | ZIP archive creation |
| `smtplib` *(stdlib)* | SMTP email sending |
| `fpdf2` | PDF generation |

## Setup

```bash
cd task-automation-suite

python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
python main.py
```

## Usage

Pick a tool from the interactive main menu:

```
[1] 📁  Bulk File Renamer
[2] 📄  PDF Report Generator
[3] 📧  Email Notifier
[4] 🗄️  Folder Backup
[5] 🚪  Exit
```

### File Renamer — Operations

| Operation | Example |
|---|---|
| Add prefix | `report_` → `report_budget.xlsx` |
| Add suffix | `_v2` → `notes_v2.txt` |
| Replace text | `old` → `new` in all filenames |
| Sequential | `photo_001.jpg`, `photo_002.jpg` … |
| Change extension | `.txt` → `.md` |
| Case convert | `lower` / `upper` / `title` |

### PDF Generator

Generates a styled dark-header PDF with:
- Report title & auto-timestamp
- Section headings
- Body text paragraphs
- Key-value info tables
- Multi-column data tables
- Page numbers in footer

### Email Notifier

- Supports Gmail and any SMTP server with STARTTLS
- HTML email with styled template (pipe-separate lines: `Item 1 | Item 2 | Item 3`)
- File attachments supported
- For Gmail, use an **App Password** (not your main password)

### Folder Backup

- Creates `backups/<name>_<timestamp>.zip`
- Lists all backups with size and creation date
- Prune to keep only the N most recent archives

## File Structure

```
task-automation-suite/
├── main.py              # CLI entry point
├── file_renamer.py      # Bulk rename operations (pathlib)
├── pdf_reporter.py      # PDF generation (fpdf2)
├── email_notifier.py    # Email sending (smtplib)
├── folder_backup.py     # ZIP backup (shutil)
├── config.py            # SMTP config persistence
├── requirements.txt     # fpdf2
├── .gitignore           # Excludes email_config.json, reports/, backups/
└── README.md            # This file
```

## Generated Files (git-ignored)

| Path | Description |
|---|---|
| `email_config.json` | SMTP credentials |
| `reports/*.pdf` | Generated PDF reports |
| `backups/*.zip` | Folder backup archives |
