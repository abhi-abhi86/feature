import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from datetime import datetime
from typing import Dict, Any

from ..core.event_bus import event_bus
from ..core.event_types import MarketEvent, NewsEvent, SignalEvent
from .main_overlay import MainOverlay

class UIManager(QObject):
    # Signals to update UI widgets safely from other threads
    pnl_updated = pyqtSignal(float, float)
    market_data_updated = pyqtSignal(str, float)
    new_signal = pyqtSignal(str)
    new_alert = pyqtSignal(str, str)
    status_updated = pyqtSignal(str, bool)

    def __init__(self, overlay: MainOverlay):
        super().__init__()
        self.overlay = overlay
        self.market_prices = {}
        self.portfolio_value = 100000.0  # Starting value
        self._connect_signals()

    def _connect_signals(self):
        """Connect UI signals to widget methods."""
        self.pnl_updated.connect(self.overlay.plot_widget.add_point)
        self.new_signal.connect(self.overlay.alert_widget.show_toast)
        self.new_alert.connect(self.overlay.alert_widget.show_popup)
        self.market_data_updated.connect(self._on_market_data_updated)
        self.status_updated.connect(self._on_status_updated)

    def _on_market_data_updated(self, ticker: str, price: float):
        """Handle market data updates."""
        self.market_prices[ticker] = price
        # For demo purposes, simulate portfolio value changes
        base_value = 100000.0
        price_factor = price / 1000.0  # Normalize price
        self.portfolio_value = base_value + (price_factor * 1000)
        
        # Update plot with current portfolio value
        timestamp = datetime.now().timestamp()
        self.pnl_updated.emit(timestamp, self.portfolio_value)

    def _on_status_updated(self, component: str, is_connected: bool):
        """Update status widget."""
        if component == "broker":
            self.overlay.status_widget.update_broker_status(is_connected)
        elif component == "news":
            self.overlay.status_widget.update_news_status(is_connected)
        elif component == "llm":
            self.overlay.status_widget.update_llm_status("OK" if is_connected else "N/A")

    def update_market_data(self, event: MarketEvent):
        """Update UI with new market data."""
        self.market_data_updated.emit(event.ticker, event.price)

    def add_signal(self, event: SignalEvent):
        """Add a new trading signal to UI."""
        message = f"Signal: {event.action} {event.ticker} at {event.price:.2f}"
        self.new_signal.emit(message)

    def update_portfolio(self, positions: Dict[str, float]):
        """Update UI with portfolio information."""
        total_value = sum(positions.values()) if positions else 0
        message = f"Portfolio updated: {len(positions)} positions, Total: ${total_value:.2f}"
        self.new_alert.emit(message, "INFO")

    def update_broker_status(self, is_connected: bool):
        """Update broker connection status."""
        self.status_updated.emit("broker", is_connected)

    def update_news_status(self, is_active: bool):
        """Update news feed status."""
        self.status_updated.emit("news", is_active)

    async def listen_for_ui_events(self):
        """
        Listens on the main event bus for events relevant to the UI.
        This method should be called as a background task.
        """
        while True:
            try:
                event = await event_bus.get()
                
                if isinstance(event, MarketEvent):
                    self.update_market_data(event)
                elif isinstance(event, SignalEvent):
                    self.add_signal(event)
                elif isinstance(event, NewsEvent):
                    message = f"News: {event.headline[:50]}..."
                    self.new_alert.emit(message, "NEWS")
                
                event_bus.task_done()
                
            except Exception as e:
                print(f"Error in UI event listener: {e}")
                await asyncio.sleep(1)
