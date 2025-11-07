#!/usr/bin/env python3
"""
UI Test script to verify the Trading Agent AI interface is working properly.
This script will create the UI components and simulate some events to test functionality.
"""

import sys
import asyncio
import os
from datetime import datetime
import random

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import qasync

from src.ui.main_overlay import MainOverlay
from src.ui.ui_manager import UIManager
from src.core.event_types import MarketEvent, SignalEvent

class UITester:
    def __init__(self):
        self.overlay = MainOverlay()
        self.ui_manager = UIManager(self.overlay)
        
    def setup_ui(self):
        """Setup the UI for testing."""
        # Show the main overlay
        self.overlay.show()
        
        # Update initial status
        self.ui_manager.update_broker_status(True)  # Demo mode
        self.ui_manager.update_news_status(True)
        
        # Setup timers for demo data
        self.setup_demo_timers()
        
    def setup_demo_timers(self):
        """Setup timers to simulate live data."""
        # Market data timer (every 2 seconds)
        self.market_timer = QTimer()
        self.market_timer.timeout.connect(self.generate_market_data)
        self.market_timer.start(2000)
        
        # Signal timer (every 10 seconds)
        self.signal_timer = QTimer()
        self.signal_timer.timeout.connect(self.generate_signal)
        self.signal_timer.start(10000)
        
        # Alert timer (every 15 seconds)
        self.alert_timer = QTimer()
        self.alert_timer.timeout.connect(self.generate_alert)
        self.alert_timer.start(15000)
        
    def generate_market_data(self):
        """Generate mock market data."""
        tickers = ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS", "INFY"]
        ticker = random.choice(tickers)
        
        # Generate realistic prices
        base_prices = {
            "NIFTY": 18000,
            "BANKNIFTY": 42000, 
            "RELIANCE": 2500,
            "TCS": 3500,
            "INFY": 1500
        }
        
        base_price = base_prices.get(ticker, 1000)
        price_change = random.uniform(-2, 2)  # ±2% change
        price = base_price + (base_price * price_change / 100)
        volume = random.randint(1000, 50000)
        
        # Create mock market event
        market_event = MarketEvent(
            timestamp=datetime.now(),
            ticker=ticker,
            price=round(price, 2),
            volume=volume
        )
        
        # Update UI with market data
        self.ui_manager.update_market_data(market_event)
        print(f"Generated market data: {ticker} @ {price:.2f}")
        
    def generate_signal(self):
        """Generate mock trading signal."""
        actions = ["BUY", "SELL"]
        tickers = ["RELIANCE", "TCS", "INFY", "WIPRO", "HDFCBANK"]
        
        action = random.choice(actions)
        ticker = random.choice(tickers)
        price = random.uniform(1000, 3000)
        
        # Create mock signal event
        signal_event = SignalEvent(
            timestamp=datetime.now(),
            ticker=ticker,
            action=action,
            price=price,
            confidence=random.uniform(0.6, 0.9)
        )
        
        # Update UI with signal
        self.ui_manager.add_signal(signal_event)
        print(f"Generated signal: {action} {ticker} @ {price:.2f}")
        
    def generate_alert(self):
        """Generate mock alerts/notifications."""
        alert_types = [
            ("Market volatility detected", "WARNING"),
            ("New trading signal generated", "INFO"),
            ("Portfolio rebalanced", "INFO"),
            ("Risk threshold reached", "ERROR"),
            ("News sentiment changed", "NEWS")
        ]
        
        message, level = random.choice(alert_types)
        self.ui_manager.new_alert.emit(message, level)
        print(f"Generated alert: [{level}] {message}")

async def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Set up the UI tester
    tester = UITester()
    tester.setup_ui()
    
    print("🎯 Trading Agent AI UI Test Started!")
    print("📊 You should see a dark overlay window with:")
    print("   • Status indicators at the top")
    print("   • Live portfolio chart")
    print("   • Popup alerts and notifications")
    print("Press Ctrl+C to stop the test")
    
    # Run the application
    try:
        # Keep the app running
        while True:
            app.processEvents()
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 UI Test stopped")
    finally:
        app.quit()

if __name__ == "__main__":
    # Run with asyncio
    asyncio.run(main())