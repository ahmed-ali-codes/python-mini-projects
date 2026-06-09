import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class DbManager:
    def __init__(self, db_path=config.DB_PATH):
        self.db_path = db_path
        self.create_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # HackerNews
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS hackernews (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        url TEXT,
                        score INTEGER,
                        comments INTEGER,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Crypto Prices
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS crypto_prices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        coin_name TEXT,
                        price_usd REAL,
                        market_cap REAL,
                        change_24h REAL,
                        volume_24h REAL,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # GitHub Trending
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS github_trending (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        repo_name TEXT,
                        description TEXT,
                        language TEXT,
                        stars_today INTEGER,
                        total_stars INTEGER,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def insert_hackernews(self, data):
        """Insert a list of HackerNews dictionaries."""
        query = """
            INSERT INTO hackernews (title, url, score, comments)
            VALUES (?, ?, ?, ?)
        """
        values = [(item.get('title'), item.get('url'), item.get('score'), item.get('comments')) for item in data]
        self._insert_many(query, values)

    def insert_crypto(self, data):
        """Insert a list of Crypto dictionaries."""
        query = """
            INSERT INTO crypto_prices (coin_name, price_usd, market_cap, change_24h, volume_24h)
            VALUES (?, ?, ?, ?, ?)
        """
        values = [(item.get('coin_name'), item.get('price_usd'), item.get('market_cap'), item.get('change_24h'), item.get('volume_24h')) for item in data]
        self._insert_many(query, values)

    def insert_github(self, data):
        """Insert a list of GitHub trending dictionaries."""
        query = """
            INSERT INTO github_trending (repo_name, description, language, stars_today, total_stars)
            VALUES (?, ?, ?, ?, ?)
        """
        values = [(item.get('repo_name'), item.get('description'), item.get('language'), item.get('stars_today'), item.get('total_stars')) for item in data]
        self._insert_many(query, values)

    def _insert_many(self, query, values):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, values)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database insertion error: {e}")

    def get_data_as_dataframe(self, table_name, limit=None):
        """Retrieve data from a table and return as a pandas DataFrame."""
        query = f"SELECT * FROM {table_name} ORDER BY scraped_at DESC"
        if limit:
            query += f" LIMIT {limit}"
            
        try:
            with self._get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                return df
        except sqlite3.Error as e:
            print(f"Error reading from {table_name}: {e}")
            return pd.DataFrame()
