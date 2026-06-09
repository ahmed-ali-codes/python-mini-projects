import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.sqlite")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Scraper configurations
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# URLs
URL_HACKERNEWS = "https://news.ycombinator.com/"
URL_GITHUB_TRENDING = "https://github.com/trending"
URL_COINGECKO_API = "https://api.coingecko.com/api/v3"

# Rate limiting
DELAY_BETWEEN_REQUESTS = 1.0 # seconds
