import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.core.sentiment import SentimentAnalyzer

class TestSentimentAnalysis(unittest.TestCase):
    def setUp(self):
        self.sentiment_analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        positive_text = "Stock market rallies to new highs, great profits expected!"
        score = self.sentiment_analyzer.get_sentiment(positive_text)
        self.assertGreater(score, 0, "Should return positive sentiment")

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        negative_text = "Market crashes, huge losses, disaster for investors!"
        score = self.sentiment_analyzer.get_sentiment(negative_text)
        self.assertLess(score, 0, "Should return negative sentiment")

    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        neutral_text = "The market is open today."
        score = self.sentiment_analyzer.get_sentiment(neutral_text)
        self.assertAlmostEqual(score, 0, delta=0.3, msg="Should return nearly neutral sentiment")

    def test_empty_text(self):
        """Test behavior with empty text."""
        score = self.sentiment_analyzer.get_sentiment("")
        self.assertEqual(score, 0.0, "Empty text should return neutral sentiment")

if __name__ == "__main__":
    unittest.main()
