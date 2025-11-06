import asyncio
import feedparser
import logging
from datetime import datetime

from ..core.config_loader import ConfigLoader
from ..core.event_bus import event_bus
from ..core.event_types import NewsEvent
from ..core.sentiment import SentimentAnalyzer
from .feed_manager import FeedManager

logger = logging.getLogger(__name__)

class RSSFetcher:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.feed_manager = FeedManager(config)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.fetch_interval = int(self.config.get_main_config("General", "news_fetch_interval_seconds", fallback=300))
        self.seen_headlines = set()

    def start(self):
        logger.info("Starting RSS Fetcher...")
        self.fetch_task = asyncio.create_task(self._fetch_loop())
        logger.info(f"RSS Fetcher started. Fetching every {self.fetch_interval} seconds.")

    async def _fetch_loop(self):
        while True:
            await self._fetch_all_feeds()
            await asyncio.sleep(self.fetch_interval)

    async def _fetch_all_feeds(self):
        feeds = self.feed_manager.get_feeds()
        for feed_url in feeds:
            try:
                parsed_feed = feedparser.parse(feed_url)
                for entry in parsed_feed.entries:
                    if entry.title not in self.seen_headlines:
                        self.seen_headlines.add(entry.title)
                        sentiment_score = self.sentiment_analyzer.get_sentiment(entry.title)
                        
                        news_event = NewsEvent(
                            timestamp=datetime.now(),
                            headline=entry.title,
                            source=parsed_feed.feed.title,
                            sentiment=sentiment_score
                        )
                        await event_bus.put(news_event)
                        logger.debug(f"Published NewsEvent: {news_event.headline}")
            except Exception as e:
                logger.error(f"Error fetching or parsing feed {feed_url}: {e}")
