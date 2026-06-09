# URL Shortener

A TinyURL-like service built with Flask and SQLite.

## Features
- Generate short links from long URLs
- Redirect users to original URLs
- Track click counts for shortened links

## Setup
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run the application: `python app.py`

## Usage
- Open `http://127.0.0.1:5000/` in your browser.
- Enter a URL to shorten.
- View stats at `http://127.0.0.1:5000/stats/<short_id>`.
