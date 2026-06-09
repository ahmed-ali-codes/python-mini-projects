# ⬇️ Multi-Threaded File Downloader

A CLI tool to download files concurrently with pause, resume, and progress tracking — built with Python's `threading`, `concurrent.futures`, and HTTP Range requests.

## Features

| Feature | Implementation |
|---|---|
| ⬇️ Large file downloads | Streaming HTTP with 64KB chunks |
| ⏸️ Pause / Resume | `threading.Event` + HTTP `Range` header |
| 📋 Parallel downloads | `concurrent.futures.ThreadPoolExecutor` |
| 💾 Resumable sessions | JSON `.session` file preserves byte offset |
| 📊 Progress bars | `tqdm` per-file progress with speed |
| 📡 Live monitor | Auto-refreshing status dashboard |

## How Pause/Resume Works

1. When a download is **paused**, a `threading.Event` blocks the write loop — the partial file is kept on disk.
2. A `.session` file records the byte offset and total size.
3. On **resume**, the downloader reads the session file and sends an HTTP `Range: bytes=<offset>-` request to continue from where it stopped.
4. This works with any server that supports HTTP Range requests (most CDNs and file servers do).

## Setup

```bash
cd multi-threaded-file-downloader

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Usage

```
[1] Add a download
[2] Add multiple downloads (parallel)
[3] View download status
[4] Live monitor (auto-refresh)
[5] Pause a download
[6] Resume a download
[7] Cancel a download
[8] Wait for all to finish
[9] Exit
```

### Example: Download 3 files simultaneously

1. Choose `[2] Add multiple downloads`
2. Enter 3 URLs one by one, then type `done`
3. Choose `[4] Live monitor` to watch progress in real time
4. Use `[5]` / `[6]` to pause and resume individual downloads

## File Structure

```
multi-threaded-file-downloader/
├── main.py               # CLI entry point
├── downloader.py         # DownloadTask: Range requests, pause/resume, tqdm
├── download_manager.py   # ThreadPoolExecutor: parallel download orchestration
├── session.py            # JSON session persistence for resume
├── requirements.txt      # requests, tqdm
├── .gitignore            # Excludes downloads/, *.session
└── README.md             # This file
```

## Key Concepts Used

- **`threading.Event`** — pauses the chunk-write loop without spinning
- **`concurrent.futures.ThreadPoolExecutor`** — runs each download in its own worker thread
- **HTTP `Range` header** — resumes from a specific byte offset
- **Streaming requests** — `stream=True` avoids loading the whole file into memory

## Generated Files (git-ignored)

| Path | Description |
|---|---|
| `downloads/` | Downloaded files |
| `*.session` | Pause/resume state files (auto-deleted on completion) |
