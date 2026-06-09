from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper
import config

class HackerNewsScraper(BaseScraper):
    def scrape(self):
        print("Scraping Hacker News...")
        html = self.fetch_html(config.URL_HACKERNEWS)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        
        # HN has a specific structure: stories are in tr.athing, metadata in the next tr
        stories = soup.find_all('tr', class_='athing')
        
        scraped_data = []
        for story in stories:
            try:
                title_tag = story.find('span', class_='titleline').find('a')
                title = title_tag.text
                url = title_tag['href']
                
                # Metadata is in the next sibling tr
                meta_row = story.find_next_sibling('tr')
                
                score_tag = meta_row.find('span', class_='score')
                score = int(score_tag.text.split()[0]) if score_tag else 0
                
                # Find comments (it's the last 'a' tag in subtext usually)
                subtext = meta_row.find('td', class_='subtext')
                comments = 0
                if subtext:
                    links = subtext.find_all('a')
                    for link in links:
                        text = link.text
                        if 'comment' in text:
                            # Extract number, e.g., '15 comments' -> 15
                            comments = int(text.split()[0])
                            break
                            
                scraped_data.append({
                    'title': title,
                    'url': url,
                    'score': score,
                    'comments': comments
                })
            except AttributeError as e:
                # Skip items that don't match the expected structure (e.g. jobs)
                continue

        print(f"Extracted {len(scraped_data)} stories from Hacker News.")
        
        if scraped_data:
            self.db_manager.insert_hackernews(scraped_data)
            print("Saved Hacker News data to database.")
