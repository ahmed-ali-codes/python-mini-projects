import time
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from database.db_manager import DbManager

class BaseScraper:
    def __init__(self):
        self.db_manager = DbManager()
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    def fetch_html(self, url):
        """Fetch HTML content from a URL with basic error handling and rate limiting."""
        try:
            time.sleep(config.DELAY_BETWEEN_REQUESTS)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def fetch_json(self, url, params=None):
        """Fetch JSON data from an API with basic error handling and rate limiting."""
        try:
            time.sleep(config.DELAY_BETWEEN_REQUESTS)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape(self):
        """Main orchestrator method to be implemented by child classes."""
        raise NotImplementedError("Subclasses must implement the scrape method.")
