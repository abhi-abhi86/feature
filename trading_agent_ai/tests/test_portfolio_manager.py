import unittest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Add src to path for testing
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.portfolio_manager.portfolio import Portfolio
from src.portfolio_manager.risk_manager import RiskManager
from src.core.event_types import SignalEvent
from datetime import datetime

class TestPortfolioManager(unittest.TestCase):
    def setUp(self):
        self.portfolio = Portfolio(initial_cash=100000)
        self.risk_manager = RiskManager(self.portfolio)

    def test_initial_portfolio_state(self):
        """Test initial portfolio state."""
        self.assertEqual(self.portfolio.get_cash(), 100000)
        self.assertEqual(len(self.portfolio.get_positions()), 0)

    def test_portfolio_buy_operation(self):
        """Test buying stocks."""
        from src.core.event_types import FillEvent
        
        fill_event = FillEvent(
            timestamp=datetime.now(),
            ticker="RELIANCE",
            action="BUY",
            quantity=10,
            price=2500,
            order_id="12345"
        )
        
        self.portfolio.on_fill(fill_event)
        
        # Check cash reduction
        expected_cash = 100000 - (10 * 2500)
        self.assertEqual(self.portfolio.get_cash(), expected_cash)
        
        # Check position
        positions = self.portfolio.get_positions()
        self.assertEqual(positions.get("RELIANCE"), 10)

    def test_risk_manager_signal_validation(self):
        """Test risk manager signal validation."""
        signal_event = SignalEvent(
            timestamp=datetime.now(),
            ticker="RELIANCE",
            signal="BUY",
            confidence=0.8,
            reason="Test signal"
        )
        
        # Test that valid signals are approved
        is_valid = self.risk_manager._is_signal_valid(signal_event)
        self.assertTrue(is_valid)

    def test_risk_manager_invalid_signal(self):
        """Test risk manager rejects invalid signals."""
        signal_event = SignalEvent(
            timestamp=datetime.now(),
            ticker="RELIANCE",
            signal="INVALID",  # Invalid signal type
            confidence=0.8,
            reason="Test signal"
        )
        
        is_valid = self.risk_manager._is_signal_valid(signal_event)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
