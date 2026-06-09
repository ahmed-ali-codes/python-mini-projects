from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper
import config

class GitHubScraper(BaseScraper):
    def scrape(self):
        print("Scraping GitHub Trending...")
        html = self.fetch_html(config.URL_GITHUB_TRENDING)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        
        # GitHub trending repos are in article tags with class Box-row
        repos = soup.find_all('article', class_='Box-row')
        
        scraped_data = []
        for repo in repos:
            try:
                # Repo name
                h2 = repo.find('h2', class_='h3')
                repo_name = h2.text.strip().replace(' ', '').replace('\n', '')
                
                # Description
                p = repo.find('p', class_='col-9')
                description = p.text.strip() if p else ""
                
                # Language
                lang_span = repo.find('span', itemprop='programmingLanguage')
                language = lang_span.text.strip() if lang_span else "Unknown"
                
                # Stars
                # Find the a tag with href ending in /stargazers
                stars_tag = repo.find('a', href=lambda h: h and h.endswith('/stargazers'))
                total_stars = 0
                if stars_tag:
                    stars_text = stars_tag.text.strip().replace(',', '')
                    total_stars = int(stars_text)
                    
                # Stars today
                stars_today = 0
                span_float_right = repo.find('span', class_='float-sm-right')
                if span_float_right and 'stars today' in span_float_right.text:
                    stars_today_text = span_float_right.text.strip().split()[0].replace(',', '')
                    stars_today = int(stars_today_text)

                scraped_data.append({
                    'repo_name': repo_name,
                    'description': description,
                    'language': language,
                    'stars_today': stars_today,
                    'total_stars': total_stars
                })
            except Exception as e:
                print(f"Error parsing a repo: {e}")
                continue

        print(f"Extracted {len(scraped_data)} trending repositories from GitHub.")
        
        if scraped_data:
            self.db_manager.insert_github(scraped_data)
            print("Saved GitHub trending data to database.")
