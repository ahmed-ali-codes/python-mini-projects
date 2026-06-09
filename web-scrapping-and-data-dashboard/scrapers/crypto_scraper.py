import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper
import config

class CryptoScraper(BaseScraper):
    def scrape(self):
        print("Scraping Crypto Prices from CoinGecko API...")
        
        url = f"{config.URL_COINGECKO_API}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 20, # Get top 20 coins
            'page': 1,
            'sparkline': False
        }
        
        data = self.fetch_json(url, params=params)
        if not data:
            return

        scraped_data = []
        for coin in data:
            scraped_data.append({
                'coin_name': coin.get('name'),
                'price_usd': coin.get('current_price'),
                'market_cap': coin.get('market_cap'),
                'change_24h': coin.get('price_change_percentage_24h'),
                'volume_24h': coin.get('total_volume')
            })

        print(f"Extracted {len(scraped_data)} coins from CoinGecko.")
        
        if scraped_data:
            self.db_manager.insert_crypto(scraped_data)
            print("Saved Crypto prices to database.")
