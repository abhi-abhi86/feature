from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text: str) -> float:
        """
        Analyze the sentiment of the given text using VADER.
        Returns a compound sentiment score between -1.0 (negative) and 1.0 (positive).
        """
        try:
            scores = self.analyzer.polarity_scores(text)
            compound_score = scores['compound']
            logger.debug(f"Sentiment analysis for text: '{text[:50]}...' -> {compound_score}")
            return compound_score
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return 0.0  # Neutral score on error
