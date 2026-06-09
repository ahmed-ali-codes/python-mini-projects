import argparse
import sys
from scrapers.hackernews_scraper import HackerNewsScraper
from scrapers.crypto_scraper import CryptoScraper
from scrapers.github_scraper import GitHubScraper
from dashboard.visualizer import Visualizer

def run_scrapers(source=None):
    if source == 'hackernews' or source == 'all':
        hn_scraper = HackerNewsScraper()
        hn_scraper.scrape()
        
    if source == 'crypto' or source == 'all':
        crypto_scraper = CryptoScraper()
        crypto_scraper.scrape()
        
    if source == 'github' or source == 'all':
        github_scraper = GitHubScraper()
        github_scraper.scrape()

def run_dashboard():
    visualizer = Visualizer()
    visualizer.generate_dashboard()

def main():
    parser = argparse.ArgumentParser(description="Web Scraping & Data Dashboard CLI")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Run data scrapers')
    scrape_parser.add_argument('--source', type=str, choices=['hackernews', 'crypto', 'github', 'all'], 
                               default='all', help='Which source to scrape')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Generate dashboard from scraped data')
    
    # All command (Scrape + Dashboard)
    subparsers.add_parser('all', help='Run all scrapers and generate dashboard')
    
    args = parser.parse_args()
    
    if args.command == 'scrape':
        run_scrapers(args.source)
    elif args.command == 'dashboard':
        run_dashboard()
    elif args.command == 'all':
        run_scrapers('all')
        run_dashboard()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
