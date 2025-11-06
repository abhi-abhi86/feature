from ..core.config_loader import ConfigLoader
from typing import List

class FeedManager:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.rss_feeds_str = self.config.get_main_config("General", "rss_feeds", fallback="")
        self.feeds = [feed.strip() for feed in self.rss_feeds_str.split(',') if feed.strip()]

    def get_feeds(self) -> List[str]:
        return self.feeds

    def add_feed(self, feed_url: str):
        if feed_url not in self.feeds:
            self.feeds.append(feed_url)
            self._save_feeds()

    def remove_feed(self, feed_url: str):
        if feed_url in self.feeds:
            self.feeds.remove(feed_url)
            self._save_feeds()

    def _save_feeds(self):
        # This method should ideally write the changes back to main_config.ini
        # For simplicity in this MVP, we are not implementing the write-back.
        # In a real application, you would use a library that can preserve
        # comments and structure in .ini files, like `configobj`.
        pass
