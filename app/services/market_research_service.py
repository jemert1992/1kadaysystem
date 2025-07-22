"""
AI-Powered Automated Market Research Service
Implements trending topic discovery, keyword analysis, and competitor scan.
Blueprint Step 1: Automates research pipeline for product idea generation.
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from collections import Counter

class MarketResearchService:
    """
    Provides trending keywords, topics, and competitor links for digital product ideation.
    """
    @staticmethod
    def scrape_trending_keywords(sources=None, max_keywords=20):
        # Example: scrape Reddit r/entrepreneur, Hacker News, Product Hunt
        sources = sources or [
            "https://www.reddit.com/r/entrepreneur/",
            "https://news.ycombinator.com/",
            "https://www.producthunt.com/",
        ]
        all_keywords = Counter()
        for url in sources:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, timeout=8)
                soup = BeautifulSoup(r.text, 'html.parser')
                # Grab headlines and links
                texts = soup.get_text(separator=' ').lower()
                keywords = re.findall(r'\b\w{5,16}\b', texts)
                all_keywords.update(keywords)
            except Exception as e:
                continue
        # Remove stopwords and common terms
        STOPWORDS = {'about','there', 'would','their','could','which', 'https', 'reddit', 'com', 'www', 'with','that','from','this','have','what','will','your','just','more', 'they','for','are'}
        keywords = [w for w, n in all_keywords.most_common() if w not in STOPWORDS]
        return keywords[:max_keywords]

    @staticmethod
    def competitor_links(domain_keywords=None, sources=None, max_competitors=10):
        # Naive: look for links on source pages containing keyword
        domain_keywords = domain_keywords or ['course','ebook','template','system','app','tool']
        sources = sources or [
            "https://www.reddit.com/r/entrepreneur/",
            "https://news.ycombinator.com/",
            "https://www.producthunt.com/",
        ]
        competitor_urls = set()
        for url in sources:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, timeout=7)
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if any(k in a.text.lower()+a['href'].lower() for k in domain_keywords):
                        competitor_urls.add(a['href'])
            except Exception:
                continue
        return list(competitor_urls)[:max_competitors]

    @staticmethod
    def summary_report():
        """Returns a package of keywords and competitors."""
        trend = MarketResearchService.scrape_trending_keywords()
        comps = MarketResearchService.competitor_links()
        return {"timestamp": datetime.utcnow().isoformat(), "trending_keywords": trend, "competitors": comps}

# Usage example:
# MarketResearchService.summary_report()
