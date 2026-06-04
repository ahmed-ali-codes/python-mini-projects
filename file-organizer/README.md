# File Organizer

A simple and efficient Python script to automatically organize files in a directory based on their file extensions. Perfect for cleaning up messy directories like your `Downloads` folder!

## Features

- **Automatically groups files:** Moves files into specific category folders (`Images`, `Documents`, `Archives`, `Audio`, `Video`, `Executables`, and `Others`).
- **Smart collision handling:** If a file with the same name already exists in the destination folder, it will intelligently rename the incoming file (e.g., `file_1.png`) to avoid overwriting your data.
- **Ignores hidden files:** Hidden files and directories (like `.DS_Store` or `.git`) are safely ignored.
- **Easy to customize:** You can easily add new extensions and categories by modifying the `FILE_CATEGORIES` dictionary in the script.

## Categories

The script currently organizes files into the following directories:
- **Images:** `.jpeg`, `.jpg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`
- **Documents:** `.pdf`, `.doc`, `.docx`, `.txt`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.csv`
- **Archives:** `.zip`, `.tar`, `.gz`, `.rar`, `.7z`
- **Audio:** `.mp3`, `.wav`, `.aac`, `.flac`
- **Video:** `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`
- **Executables:** `.exe`, `.dmg`, `.pkg`, `.deb`

*Any files that do not match these categories will be moved to an `Others` folder.*

## Prerequisites

- Python 3.x (No external libraries required; uses built-in modules `os`, `shutil`, and `argparse`).

## Usage

You can run the script from the command line, providing the target directory as an argument.

```bash
# Organize a specific directory (e.g., your Downloads folder)
python organizer.py /path/to/your/Downloads

# Organize the current working directory
python organizer.py
```

## How it Works

The script leverages Python's built-in `os` and `shutil` modules. 
1. It scans the target directory for all files.
2. It extracts each file's extension.
3. It creates destination folders (like `Images` or `Documents`) if they don't already exist.
4. It moves the files into their respective folders safely.
