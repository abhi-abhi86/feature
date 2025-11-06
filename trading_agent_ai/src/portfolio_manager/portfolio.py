import logging
from typing import Dict

from ..core.event_bus import event_bus
from ..core.event_types import FillEvent

logger = logging.getLogger(__name__)

class Portfolio:
    def __init__(self, initial_cash: float = 100000.0):
        self.cash = initial_cash
        self.positions: Dict[str, float] = {}  # Ticker -> Quantity
        self.holdings_value = 0.0

    def start(self):
        logger.info("Starting Portfolio Manager...")
        # In a real app, you might load initial positions from the database
        logger.info(f"Initial cash: {self.cash}")

    def on_fill(self, event: FillEvent):
        """
        Updates the portfolio based on a fill event.
        """
        if event.action == 'BUY':
            cost = event.price * event.quantity
            if self.cash >= cost:
                self.cash -= cost
                self.positions[event.ticker] = self.positions.get(event.ticker, 0) + event.quantity
                logger.info(f"BOUGHT {event.quantity} of {event.ticker} at {event.price}")
            else:
                logger.error("Insufficient cash to execute buy order.")
        elif event.action == 'SELL':
            if self.positions.get(event.ticker, 0) >= event.quantity:
                self.cash += event.price * event.quantity
                self.positions[event.ticker] -= event.quantity
                if self.positions[event.ticker] == 0:
                    del self.positions[event.ticker]
                logger.info(f"SOLD {event.quantity} of {event.ticker} at {event.price}")
            else:
                logger.error(f"Not enough holdings to sell {event.quantity} of {event.ticker}")
        
        self.log_portfolio_status()

    def log_portfolio_status(self):
        logger.info(f"Portfolio Status: Cash = {self.cash:.2f}, Holdings = {self.positions}")

    def get_positions(self) -> Dict[str, float]:
        return self.positions

    def get_cash(self) -> float:
        return self.cash
