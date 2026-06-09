import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from database.db_manager import DbManager

class Visualizer:
    def __init__(self):
        self.db_manager = DbManager()
        # Set a dark theme for a modern dashboard look
        plt.style.use('dark_background')
        
    def generate_dashboard(self):
        print("Generating Data Dashboard...")
        
        # Create a large figure with subplots
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('Data Scraper Dashboard', fontsize=24, fontweight='bold', color='white', y=0.98)
        
        # 1. Hacker News Top Stories (Top Left)
        ax1 = plt.subplot(2, 2, 1)
        self._plot_hackernews(ax1)
        
        # 2. Crypto Prices (Top Right)
        ax2 = plt.subplot(2, 2, 2)
        self._plot_crypto_prices(ax2)
        
        # 3. Crypto 24h Change (Bottom Left)
        ax3 = plt.subplot(2, 2, 3)
        self._plot_crypto_change(ax3)
        
        # 4. GitHub Trending Languages (Bottom Right)
        ax4 = plt.subplot(2, 2, 4)
        self._plot_github_languages(ax4)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Save dashboard
        output_path = os.path.join(config.OUTPUT_DIR, 'dashboard.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#111111')
        print(f"Dashboard saved to: {output_path}")
        plt.close()

    def _plot_hackernews(self, ax):
        df = self.db_manager.get_data_as_dataframe('hackernews', limit=15)
        if df.empty:
            ax.text(0.5, 0.5, 'No Hacker News Data', ha='center', va='center', fontsize=14)
            return
            
        # Sort by score ascending for horizontal bar chart
        df = df.sort_values(by='score', ascending=True)
        
        # Truncate titles if too long
        titles = [t[:40] + '...' if len(t) > 40 else t for t in df['title']]
        
        bars = ax.barh(titles, df['score'], color='#ff6600') # HN Orange
        ax.set_title('Top Hacker News Stories by Score', fontsize=14, pad=15)
        ax.set_xlabel('Score')
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        
        # Add values at the end of bars
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    va='center', fontsize=9, color='lightgray')

    def _plot_crypto_prices(self, ax):
        df = self.db_manager.get_data_as_dataframe('crypto_prices', limit=10)
        if df.empty:
            ax.text(0.5, 0.5, 'No Crypto Data', ha='center', va='center', fontsize=14)
            return
            
        # Sort by price descending
        df = df.sort_values(by='price_usd', ascending=False)
        
        bars = ax.bar(df['coin_name'], df['price_usd'], color='#00d2ff')
        ax.set_title('Top Cryptocurrencies by Price (USD)', fontsize=14, pad=15)
        ax.set_ylabel('Price ($)')
        ax.set_yscale('log') # Log scale is better for crypto prices
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.3)

    def _plot_crypto_change(self, ax):
        df = self.db_manager.get_data_as_dataframe('crypto_prices', limit=15)
        if df.empty:
            ax.text(0.5, 0.5, 'No Crypto Data', ha='center', va='center', fontsize=14)
            return
            
        # Sort by 24h change
        df = df.sort_values(by='change_24h', ascending=True)
        
        # Colors: Green for positive, Red for negative
        colors = ['#ff3333' if x < 0 else '#33cc33' for x in df['change_24h']]
        
        bars = ax.barh(df['coin_name'], df['change_24h'], color=colors)
        ax.set_title('Cryptocurrency 24h Price Change (%)', fontsize=14, pad=15)
        ax.set_xlabel('Change (%)')
        
        # Add zero line
        ax.axvline(0, color='white', linewidth=1, alpha=0.5)
        ax.grid(axis='x', linestyle='--', alpha=0.3)

    def _plot_github_languages(self, ax):
        df = self.db_manager.get_data_as_dataframe('github_trending', limit=25)
        if df.empty:
            ax.text(0.5, 0.5, 'No GitHub Data', ha='center', va='center', fontsize=14)
            return
            
        # Count occurrences of each language
        lang_counts = df['language'].value_counts()
        
        # Filter out "Unknown" or small slices if there are too many
        if len(lang_counts) > 7:
            top_langs = lang_counts[:6]
            other = pd.Series({'Other': lang_counts[6:].sum()})
            lang_counts = pd.concat([top_langs, other])
            
        # Custom colors for pie chart
        colors = ['#2b7489', '#3b9ab2', '#78b7c5', '#ebcc2a', '#e1af00', '#f21a00', '#aaaaaa']
        
        wedges, texts, autotexts = ax.pie(
            lang_counts, 
            labels=lang_counts.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(lang_counts)],
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True}
        )
        
        # Style the text inside the pie
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax.set_title('Trending Languages on GitHub', fontsize=14, pad=15)
